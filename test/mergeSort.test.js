const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const { mergeSort } = require("../src/mergeSort.js");

describe("mergeSort", () => {
  it("returns empty array for empty input", () => {
    assert.deepEqual(mergeSort([]), []);
  });

  it("returns single-element array unchanged", () => {
    assert.deepEqual(mergeSort([42]), [42]);
  });

  it("sorts numbers including negatives and duplicates", () => {
    assert.deepEqual(
      mergeSort([3, 1, 4, 1, 5, -9, 2, 6, 5]),
      [-9, 1, 1, 2, 3, 4, 5, 5, 6]
    );
  });

  it("is stable for equal keys (left segment order preserved)", () => {
    const rows = [
      { k: 1, id: "a" },
      { k: 2, id: "b" },
      { k: 2, id: "c" },
      { k: 1, id: "d" },
    ];
    const sorted = mergeSort(rows, (x, y) => x.k - y.k);
    assert.deepEqual(
      sorted.map((r) => r.id),
      ["a", "d", "b", "c"]
    );
  });

  it("supports custom comparator (descending)", () => {
    assert.deepEqual(mergeSort([1, 9, 2], (a, b) => b - a), [9, 2, 1]);
  });

  it("does not mutate the original array", () => {
    const original = [3, 1, 2];
    const copy = [...original];
    mergeSort(original);
    assert.deepEqual(original, copy);
  });
});
