"""
Merkle Tree implementation and test program.

A Merkle tree is a binary tree where every leaf node contains the hash of a
data block and every non-leaf node contains the cryptographic hash of its
children's hashes.  The root hash (Merkle root) summarises all data in the
tree and lets anyone verify membership without downloading the full dataset.
"""

import hashlib
import unittest


# ---------------------------------------------------------------------------
# Merkle Tree implementation
# ---------------------------------------------------------------------------

def _hash(data: str) -> str:
    """Return the SHA-256 hex digest of *data*."""
    return hashlib.sha256(data.encode()).hexdigest()


class MerkleNode:
    """A single node in a Merkle tree."""

    def __init__(self, left=None, right=None, data: str = ""):
        self.left: "MerkleNode | None" = left
        self.right: "MerkleNode | None" = right

        if left is None and right is None:
            # Leaf node — hash the raw data
            self.hash: str = _hash(data)
        else:
            combined = (left.hash if left else "") + (right.hash if right else "")
            self.hash = _hash(combined)

    def __repr__(self) -> str:  # pragma: no cover
        return f"MerkleNode(hash={self.hash[:10]}...)"


class MerkleTree:
    """Build a Merkle tree from a list of string data blocks."""

    def __init__(self, data_blocks: list[str]):
        if not data_blocks:
            raise ValueError("Cannot build a Merkle tree from an empty list.")

        # Build leaf nodes
        leaves = [MerkleNode(data=block) for block in data_blocks]
        self.root = self._build(leaves)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @staticmethod
    def _build(nodes: list[MerkleNode]) -> MerkleNode:
        """Recursively pair nodes until only the root remains."""
        if len(nodes) == 1:
            return nodes[0]

        # Duplicate the last node if the count is odd (standard approach)
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])

        parents: list[MerkleNode] = []
        for i in range(0, len(nodes), 2):
            parents.append(MerkleNode(left=nodes[i], right=nodes[i + 1]))

        return MerkleTree._build(parents)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    @property
    def root_hash(self) -> str:
        """Return the Merkle root hash."""
        return self.root.hash

    def get_proof(self, index: int, data_blocks: list[str]) -> list[dict]:
        """
        Return the Merkle proof (audit path) for the leaf at *index*.

        Each element of the returned list is a dict with keys:
            - ``"hash"``      – sibling hash
            - ``"position"``  – ``"left"`` or ``"right"`` (sibling's position)
        """
        if not (0 <= index < len(data_blocks)):
            raise IndexError(
                f"index {index} is out of range for {len(data_blocks)} data block(s)."
            )
        leaves = [MerkleNode(data=block) for block in data_blocks]
        proof: list[dict] = []
        self._collect_proof(leaves, index, proof)
        return proof

    @staticmethod
    def _collect_proof(nodes: list[MerkleNode], index: int, proof: list[dict]) -> None:
        if len(nodes) == 1:
            return

        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])

        parents: list[MerkleNode] = []
        for i in range(0, len(nodes), 2):
            parents.append(MerkleNode(left=nodes[i], right=nodes[i + 1]))

        if index % 2 == 0:
            sibling_index = index + 1
            proof.append({"hash": nodes[sibling_index].hash, "position": "right"})
        else:
            sibling_index = index - 1
            proof.append({"hash": nodes[sibling_index].hash, "position": "left"})

        MerkleTree._collect_proof(parents, index // 2, proof)

    @staticmethod
    def verify_proof(leaf_data: str, proof: list[dict], root_hash: str) -> bool:
        """
        Verify that *leaf_data* belongs to the tree whose root is *root_hash*
        using the supplied *proof*.
        """
        current_hash = _hash(leaf_data)
        for step in proof:
            if step["position"] == "right":
                current_hash = _hash(current_hash + step["hash"])
            else:
                current_hash = _hash(step["hash"] + current_hash)
        return current_hash == root_hash


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestMerkleTree(unittest.TestCase):

    def setUp(self):
        self.data = ["block_A", "block_B", "block_C", "block_D"]
        self.tree = MerkleTree(self.data)

    # --- construction ---

    def test_root_hash_is_string(self):
        self.assertIsInstance(self.tree.root_hash, str)

    def test_root_hash_length(self):
        """SHA-256 hex digest is always 64 characters."""
        self.assertEqual(len(self.tree.root_hash), 64)

    def test_root_hash_deterministic(self):
        """Same input must always produce the same root hash."""
        tree2 = MerkleTree(self.data)
        self.assertEqual(self.tree.root_hash, tree2.root_hash)

    def test_root_hash_changes_on_data_change(self):
        """Altering one leaf must change the root hash."""
        modified = ["block_A", "block_B", "block_C", "TAMPERED"]
        tree_modified = MerkleTree(modified)
        self.assertNotEqual(self.tree.root_hash, tree_modified.root_hash)

    def test_single_element_tree(self):
        tree = MerkleTree(["only"])
        self.assertEqual(len(tree.root_hash), 64)

    def test_two_element_tree(self):
        tree = MerkleTree(["a", "b"])
        self.assertEqual(len(tree.root_hash), 64)

    def test_odd_number_of_leaves(self):
        """Trees with an odd number of leaves should not raise."""
        tree = MerkleTree(["x", "y", "z"])
        self.assertEqual(len(tree.root_hash), 64)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            MerkleTree([])

    # --- proof generation & verification ---

    def test_proof_verify_first_leaf(self):
        proof = self.tree.get_proof(0, self.data)
        self.assertTrue(
            MerkleTree.verify_proof(self.data[0], proof, self.tree.root_hash)
        )

    def test_proof_verify_last_leaf(self):
        proof = self.tree.get_proof(3, self.data)
        self.assertTrue(
            MerkleTree.verify_proof(self.data[3], proof, self.tree.root_hash)
        )

    def test_proof_verify_middle_leaf(self):
        proof = self.tree.get_proof(1, self.data)
        self.assertTrue(
            MerkleTree.verify_proof(self.data[1], proof, self.tree.root_hash)
        )

    def test_proof_rejects_tampered_data(self):
        proof = self.tree.get_proof(0, self.data)
        self.assertFalse(
            MerkleTree.verify_proof("tampered_data", proof, self.tree.root_hash)
        )

    def test_proof_rejects_wrong_root(self):
        proof = self.tree.get_proof(0, self.data)
        self.assertFalse(
            MerkleTree.verify_proof(self.data[0], proof, "a" * 64)
        )

    def test_get_proof_out_of_range_raises(self):
        """get_proof() must raise IndexError for out-of-range indices."""
        with self.assertRaises(IndexError):
            self.tree.get_proof(len(self.data), self.data)  # index == len
        with self.assertRaises(IndexError):
            self.tree.get_proof(-1, self.data)  # negative index

    def test_proof_odd_tree(self):
        data = ["a", "b", "c"]
        tree = MerkleTree(data)
        for i in range(len(data)):
            proof = tree.get_proof(i, data)
            self.assertTrue(MerkleTree.verify_proof(data[i], proof, tree.root_hash))

    # --- hash function ---

    def test_hash_output_length(self):
        self.assertEqual(len(_hash("hello")), 64)

    def test_hash_known_value(self):
        expected = hashlib.sha256(b"abc").hexdigest()
        self.assertEqual(_hash("abc"), expected)


# ---------------------------------------------------------------------------
# Demo (run directly)
# ---------------------------------------------------------------------------

def demo():
    blocks = ["Transaction A", "Transaction B", "Transaction C", "Transaction D"]
    tree = MerkleTree(blocks)

    print("=== Merkle Tree Demo ===")
    print(f"Data blocks : {blocks}")
    print(f"Merkle root : {tree.root_hash}\n")

    idx = 1
    proof = tree.get_proof(idx, blocks)
    print(f"Proof for '{blocks[idx]}':")
    for step in proof:
        print(f"  sibling ({step['position']}): {step['hash'][:16]}...")

    valid = MerkleTree.verify_proof(blocks[idx], proof, tree.root_hash)
    print(f"\nProof valid? {valid}")

    tampered = MerkleTree.verify_proof("Tampered data", proof, tree.root_hash)
    print(f"Tampered proof valid? {tampered}")


if __name__ == "__main__":
    demo()
    print("\n=== Running unit tests ===\n")
    unittest.main(argv=[""], exit=False, verbosity=2)
