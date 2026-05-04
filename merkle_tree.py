"""Minimal binary Merkle tree over SHA-256 (odd levels duplicate the last hash)."""

from __future__ import annotations

import hashlib
from typing import List, Sequence


def _leaf_hash(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()


def _node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


class MerkleTree:
    """Build a Merkle root from leaf payloads (pre-images)."""

    def __init__(self, leaves: Sequence[bytes]) -> None:
        if not leaves:
            raise ValueError("MerkleTree requires at least one leaf")
        self._leaf_data: List[bytes] = list(leaves)
        self._layers: List[List[bytes]] = self._build_layers(self._leaf_data)

    @staticmethod
    def _build_layers(leaf_data: Sequence[bytes]) -> List[List[bytes]]:
        layer: List[bytes] = [_leaf_hash(d) for d in leaf_data]
        layers: List[List[bytes]] = [layer]
        while len(layer) > 1:
            nxt: List[bytes] = []
            for i in range(0, len(layer), 2):
                left = layer[i]
                right = layer[i + 1] if i + 1 < len(layer) else layer[i]
                nxt.append(_node_hash(left, right))
            layer = nxt
            layers.append(layer)
        return layers

    @property
    def root(self) -> bytes:
        return self._layers[-1][0]

    def layers(self) -> List[List[bytes]]:
        """Copy of internal layers (leaf hashes up to root)."""
        return [list(x) for x in self._layers]
