"""Tests for merkle_tree.MerkleTree (stdlib unittest)."""

from __future__ import annotations

import hashlib
import unittest

from merkle_tree import MerkleTree, _leaf_hash, _node_hash


class TestMerkleTree(unittest.TestCase):
    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            MerkleTree([])

    def test_single_leaf_root_matches_leaf_hash(self) -> None:
        data = b"only-one"
        tree = MerkleTree([data])
        self.assertEqual(tree.root, _leaf_hash(data))

    def test_two_leaves_manual_root(self) -> None:
        a, b = b"left", b"right"
        tree = MerkleTree([a, b])
        expected = _node_hash(_leaf_hash(a), _leaf_hash(b))
        self.assertEqual(tree.root, expected)

    def test_three_leaves_duplicates_last_on_level(self) -> None:
        chunks = [b"a", b"b", b"c"]
        tree = MerkleTree(chunks)
        L0 = [_leaf_hash(chunks[0]), _leaf_hash(chunks[1]), _leaf_hash(chunks[2])]
        # Level 1: (h0,h1), (h2,h2 duplicate)
        L1 = [_node_hash(L0[0], L0[1]), _node_hash(L0[2], L0[2])]
        root = _node_hash(L1[0], L1[1])
        self.assertEqual(tree.root, root)

    def test_deterministic_same_inputs(self) -> None:
        leaves = [b"x", b"y", b"z", b"w"]
        self.assertEqual(MerkleTree(leaves).root, MerkleTree(leaves).root)

    def test_root_hex_stable_fixture(self) -> None:
        """Golden-vector style check: root hex for a fixed tuple of leaves."""
        leaves = [b"alpha", b"beta"]
        root = MerkleTree(leaves).root
        self.assertEqual(
            root.hex(),
            hashlib.sha256(b"\x01" + _leaf_hash(leaves[0]) + _leaf_hash(leaves[1])).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
