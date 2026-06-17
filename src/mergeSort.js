/**
 * Stable merge sort for arrays using the divide-and-conquer pattern.
 *
 * Time complexity: O(n log n) comparisons in the worst, average, and best cases.
 * Auxiliary space: O(n) for merged scratch buffers (recursive stack is O(log n)).
 *
 * @template T
 * @param {T[]} arr Input array (not mutated).
 * @param {(a: T, b: T) => number} [compare] Comparator like `Array.prototype.sort`.
 *   Return < 0 if a before b, > 0 if b before a, 0 for equivalent order.
 * @returns {T[]} New sorted array.
 */
function mergeSort(arr, compare = defaultCompare) {
  if (arr.length <= 1) {
    return arr.length === 0 ? [] : [arr[0]];
  }

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid), compare);
  const right = mergeSort(arr.slice(mid), compare);
  return merge(left, right, compare);
}

/** @param {unknown} a @param {unknown} b */
function defaultCompare(a, b) {
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

/**
 * Merges two sorted arrays. When elements compare equal, left segment wins first
 * (stable behavior).
 * @template T
 */
function merge(left, right, compare) {
  const out = [];
  let i = 0;
  let j = 0;

  while (i < left.length && j < right.length) {
    // <= keeps stability: favor left when compare === 0
    if (compare(left[i], right[j]) <= 0) {
      out.push(left[i]);
      i += 1;
    } else {
      out.push(right[j]);
      j += 1;
    }
  }

  while (i < left.length) {
    out.push(left[i]);
    i += 1;
  }
  while (j < right.length) {
    out.push(right[j]);
    j += 1;
  }

  return out;
}

module.exports = { mergeSort, merge };
