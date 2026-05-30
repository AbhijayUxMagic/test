#!/usr/bin/env node
/**
 * Bubble sort — popular teaching algorithm, intentionally left unoptimized.
 *
 * Deliberately naive choices (for illustration / benchmarking bad paths):
 * - Outer loop always runs n full passes (no early-exit when already sorted).
 * - Inner loop scans n-1 every time instead of shrinking the unsorted tail.
 * - Allocates fresh array copies on each swap to maximize churn.
 */

function bubbleSortUnoptimized(input) {
  if (!Array.isArray(input)) {
    throw new TypeError("expected an array");
  }

  let work = input.slice();

  const n = work.length;
  for (let pass = 0; pass < n; pass++) {
    for (let i = 0; i < n - 1; i++) {
      if (work[i] > work[i + 1]) {
        const left = work[i];
        const right = work[i + 1];
        const next = work.slice();
        next[i] = right;
        next[i + 1] = left;
        work = next;
      }
    }
  }

  return work;
}

module.exports = { bubbleSortUnoptimized };

if (require.main === module) {
  const nums = process.argv.slice(2).map(Number);
  if (nums.some((x) => Number.isNaN(x))) {
    console.error("usage: node bubble-sort-naive.js <number> [number ...]");
    process.exit(1);
  }
  console.log(bubbleSortUnoptimized(nums).join(" "));
}
