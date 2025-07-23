/**
 * Sorts an array using insertion sort.
 * This algorithm is efficient for small arrays.
 *
 * @param {Array} arr The array to sort.
 * @param {number} left The starting index.
 * @param {number} right The ending index.
 */
function insertionSort(arr, left = 0, right = arr.length - 1) {
    for (let i = left + 1; i <= right; i++) {
    const key = arr[i];
    let j = i - 1;
    while (j >= left && arr[j] > key) {
        arr[j + 1] = arr[j];
        j--;
    }
    arr[j + 1] = key;
    }
    return arr;
}

/**
 * Partitions the array for Quicksort.
 *
 * @param {Array} arr The array to partition.
 * @param {number} low The starting index.
 * @param {number} high The ending index.
 * @returns {number} The partition index (the pivot's final position).
 */
function partition(arr, low, high) {
    const pivot = arr[high];
    let i = low - 1;
    for (let j = low; j < high; j++) {
    if (arr[j] < pivot) {
        i++;
      [arr[i], arr[j]] = [arr[j], arr[i]]; // Swap elements
    }
    }
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    return i + 1;
}

/**
 * The main function that implements the hybrid sort algorithm.
 * It uses Quicksort for larger partitions and switches to Insertion Sort
 * for smaller ones.
 *
 * @param {Array} arr The array to sort.
 * @param {number} low The starting index.
 * @param {number} high The ending index.
 */
function hybridSort(arr, low = 0, high = arr.length - 1) {
    const INSERTION_SORT_THRESHOLD = 10;

    while (low < high) {
    // If the partition size is small, use Insertion Sort
    if (high - low + 1 < INSERTION_SORT_THRESHOLD) {
        insertionSort(arr, low, high);
        break;
    }

    const pi = partition(arr, low, high);

    // Recurse on the smaller partition first to optimize tail recursion
    if (pi - low < high - pi) {
        hybridSort(arr, low, pi - 1);
        low = pi + 1;
    } else {
        hybridSort(arr, pi + 1, high);
        high = pi - 1;
    }
  }
}

// --- Example Usage ---
const arrayToSort = [10, 7, 8, 9, 1, 5, 12, 3, 2, 4, 6, 11, 13];
console.log("Original array:", arrayToSort);

hybridSort(arrayToSort);

console.log("Sorted array:", arrayToSort);

// --- Performance Test ---
const largeArray = Array.from({ length: 10000 }, () => Math.floor(Math.random() * 100000));
const largeArrayCopy1 = [...largeArray];
const largeArrayCopy2 = [...largeArray];

console.log("\n--- Performance Comparison ---");

// Test Hybrid Sort
console.time("Hybrid Sort");
hybridSort(largeArrayCopy1);
console.timeEnd("Hybrid Sort");

// Test native Array.prototype.sort (often a highly optimized quicksort or similar)
console.time("Native Sort");
largeArrayCopy2.sort((a, b) => a - b);
console.timeEnd("Native Sort");
