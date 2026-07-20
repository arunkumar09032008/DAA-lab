"""
Divide-and-conquer Min/Max finder, compared against a naive linear scan.

The classic result: a naive scan needs ~2n comparisons to find both the
min and the max of an array, while the divide-and-conquer approach only
needs ~3n/2 - 2 comparisons.
"""

import random


def min_max_dc(arr, low, high, counter):
    """Recursively find (min, max) of arr[low..high].

    `counter` is a single-element list used as a mutable int so the
    comparison count can be accumulated across recursive calls without
    relying on a module-level global (safer for concurrent/web use).
    """
    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        counter[0] += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid, counter)
    rmin, rmax = min_max_dc(arr, mid + 1, high, counter)

    # Conquer: combine with 2 comparisons
    counter[0] += 1
    overall_min = lmin if lmin < rmin else rmin
    counter[0] += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def find_min_max_dc(arr):
    """Convenience wrapper: returns (min, max, comparison_count)."""
    if not arr:
        raise ValueError("Array must be non-empty")
    counter = [0]
    mn, mx = min_max_dc(arr, 0, len(arr) - 1, counter)
    return mn, mx, counter[0]


def find_min_max_naive(arr):
    """Naive linear scan: returns (min, max, comparison_count)."""
    if not arr:
        raise ValueError("Array must be non-empty")
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps


def run_demo():
    """Runs the small demo + performance table, returns results as data."""
    results = {}

    arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]
    mn, mx, dc_comps = find_min_max_dc(arr)
    _, _, naive_comps = find_min_max_naive(arr)

    results["demo"] = {
        "array": arr,
        "min": mn,
        "max": mx,
        "dc_comparisons": dc_comps,
        "naive_comparisons": naive_comps,
    }

    table = []
    for size in [10, 100, 1000, 10000]:
        rand_arr = [random.randint(1, 10000) for _ in range(size)]
        _, _, dc = find_min_max_dc(rand_arr)
        _, _, naive = find_min_max_naive(rand_arr)
        formula = 3 * size // 2 - 2
        table.append(
            {
                "size": size,
                "dc_comparisons": dc,
                "naive_comparisons": naive,
                "formula_3n_2_minus_2": formula,
            }
        )

    results["performance"] = table
    return results


if __name__ == "__main__":
    data = run_demo()

    demo = data["demo"]
    print(f"Array: {demo['array']}")
    print(f"Min: {demo['min']}, Max: {demo['max']}")
    print(f"D&C Comparisons: {demo['dc_comparisons']}")
    print(f"Naive Comparisons: {demo['naive_comparisons']}")

    print(f'\n{"Size":>8} {"DC Comps":>12} {"Naive Comps":>14} {"Formula 3n/2-2":>16}')
    print("-" * 56)
    for row in data["performance"]:
        print(
            f"{row['size']:>8} {row['dc_comparisons']:>12} "
            f"{row['naive_comparisons']:>14} {row['formula_3n_2_minus_2']:>16}"
        )
