import assert from "node:assert/strict";
import test from "node:test";
import { mergeSort } from "./mergeSort.js";

test("empty array", () => {
  assert.deepEqual(mergeSort([]), []);
});

test("single element", () => {
  assert.deepEqual(mergeSort([42]), [42]);
});

test("unsorted numbers including negatives and duplicates", () => {
  assert.deepEqual(
    mergeSort([3, -1, 4, 1, -1, 5, 9, 2, 6]),
    [-1, -1, 1, 2, 3, 4, 5, 6, 9],
  );
});

test("already sorted", () => {
  assert.deepEqual(mergeSort([1, 2, 3]), [1, 2, 3]);
});

test("reverse sorted", () => {
  assert.deepEqual(mergeSort([3, 2, 1]), [1, 2, 3]);
});

test("custom comparator (descending)", () => {
  const desc = (a, b) => b - a;
  assert.deepEqual(mergeSort([1, 5, 2], desc), [5, 2, 1]);
});

test("does not mutate input", () => {
  const input = [2, 1];
  const copy = [...input];
  mergeSort(input);
  assert.deepEqual(input, copy);
});
