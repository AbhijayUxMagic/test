/**
 * Optimized Bubble Sort (JavaScript)
 *
 * Optimizations:
 * 1. Early exit if no swaps occur in a pass (array is already sorted).
 * 2. Reduces the inner loop bound each pass since the largest element
 *    bubbles to the end.
 *
 * Time Complexity:
 *   - Best:    O(n)   — already sorted
 *   - Average: O(n²)
 *   - Worst:   O(n²)
 * Space Complexity: O(1) — in-place
 */

function bubbleSort(arr) {
  const n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    let swapped = false;

    // Last i elements are already in place
    for (let j = 0; j < n - 1 - i; j++) {
      if (arr[j] > arr[j + 1]) {
        // Swap adjacent elements
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        swapped = true;
      }
    }

    // No swaps in this pass — array is sorted
    if (!swapped) break;
  }
  return arr;
}

// ── Example Usage ─────────────────────────────────────────────────────────────
const numbers = [64, 34, 25, 12, 22, 11, 90];
console.log("Original array: ", numbers);
console.log("Sorted array:  ", bubbleSort([...numbers]));

// Edge cases
console.log("Empty array:   ", bubbleSort([]));
console.log("Single element:", bubbleSort([42]));
console.log("Already sorted:", bubbleSort([1, 2, 3, 4, 5]));
console.log("Reverse sorted:", bubbleSort([5, 4, 3, 2, 1]));
