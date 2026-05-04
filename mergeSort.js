/**
 * Stable merge sort for arrays.
 *
 * Time complexity: O(n log n) comparisons in the worst case.
 * Auxiliary space: O(n) for the merge buffer, plus O(log n) call stack depth.
 *
 * @param {Array} arr - Elements to sort (not mutated; a new array is returned).
 * @param {(a: unknown, b: unknown) => number} [compare] - Like `Array#sort`:
 *   return < 0 if a before b, > 0 if b before a, 0 if equal.
 *   Defaults to numeric comparison for numbers, else lexicographic via String().
 * @returns {Array} A new sorted array.
 */
export function mergeSort(arr, compare = defaultCompare) {
  const n = arr.length;
  if (n <= 1) {
    return n === 0 ? [] : [arr[0]];
  }

  const a = arr.slice();
  const aux = new Array(n);

  function sortRange(left, right) {
    // [left, right) — half-open interval
    if (right - left <= 1) {
      return;
    }
    const mid = left + Math.floor((right - left) / 2);
    sortRange(left, mid);
    sortRange(mid, right);

    let i = left;
    let j = mid;
    let k = left;
    while (i < mid && j < right) {
      if (compare(a[i], a[j]) <= 0) {
        aux[k++] = a[i++];
      } else {
        aux[k++] = a[j++];
      }
    }
    while (i < mid) {
      aux[k++] = a[i++];
    }
    while (j < right) {
      aux[k++] = a[j++];
    }
    for (let t = left; t < right; t++) {
      a[t] = aux[t];
    }
  }

  sortRange(0, n);
  return a;
}

function defaultCompare(a, b) {
  if (typeof a === "number" && typeof b === "number") {
    return a - b;
  }
  return String(a).localeCompare(String(b));
}
