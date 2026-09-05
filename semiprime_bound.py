import math
import time
from typing import Tuple, Optional, List


class SemiprimeBound:
    """
    Implements the N-only upper bound on the factor sum (p + q) of an odd
    semiprime N = pq, as formulated by Giri Venkatesh (2026).

    Theorem:
        S = p + q < sqrt(N) + N/c
    valid whenever the smaller prime factor p > c.

    p > c is established using only divisibility checks on N (no factoring).
    """

    DEFAULT_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    def verify_c_threshold(self, N: int, c: int = 20, primes_to_check: Optional[List[int]] = None) -> bool:
        """
        Confirms p > c holds for N, using only divisibility checks (no factoring).

        Signature configuration: c = 20, verified via the seven-prime check
        {3, 5, 7, 11, 13, 17, 19}. If none of these divide N, the smaller factor
        p must be >= 23 > 20, satisfying p > c.
        """
        if primes_to_check is None:
            primes_to_check = self.DEFAULT_PRIMES

        relevant_primes = [p for p in primes_to_check if p <= c]
        return all(N % p != 0 for p in relevant_primes)

    def compute_bound(self, N: int, c: int = 20, verify: bool = True) -> float:
        """
        Computes S = p + q < sqrt(N) + N/c.

        If verify=True, first checks (via verify_c_threshold) that p > c holds
        for this N before returning the bound; raises if not established.
        """
        if N % 2 == 0:
            raise ValueError("N must be an odd semiprime.")

        if verify and not self.verify_c_threshold(N, c=c):
            raise ValueError(
                f"Cannot certify p > {c} for N={N} via divisibility checks; "
                f"bound not guaranteed to hold with this c."
            )

        return math.sqrt(N) + (N / c)

    def auto_bound(self, candidate_primes: Optional[List[int]] = None, N: int = None) -> Tuple[float, int]:
        """
        Automatically finds the tightest usable c for this N by walking up
        through candidate_primes and taking the largest prime that still
        certifies p > c, then returns the resulting bound.

        Returns (bound, c_used).
        """
        if candidate_primes is None:
            candidate_primes = self.DEFAULT_PRIMES

        best_c = 2  # trivial floor if nothing else is certifiable
        for prime in candidate_primes:
            if self.verify_c_threshold(N, c=prime, primes_to_check=candidate_primes):
                best_c = prime
            else:
                break

        return self.compute_bound(N, c=best_c), best_c

    @staticmethod
    def brute_force_factor(N: int) -> Tuple[int, int]:
        """Trial division baseline used only for verification, not by the bound itself."""
        for i in range(3, int(math.sqrt(N)) + 1, 2):
            if N % i == 0:
                return i, N // i
        raise ValueError("N is prime or not an odd composite.")


# ==========================================
# TEST AND VERIFICATION SUITE
# ==========================================
if __name__ == "__main__":
    bound_calc = SemiprimeBound()

    test_cases = [
        667,           # p=23, q=29
        247,           # p=13, q=19
        143,           # p=11, q=13
        1000000007 * 23,  # large N, small p
        23000000207,   # large N, small p
    ]

    print("=" * 80)
    print("GIRI VENKATESH (2026) - SEMIPRIME FACTOR-SUM BOUND VERIFICATION")
    print("=" * 80)

    for N in test_cases:
        print(f"\nAnalyzing N = {N}")

        p, q = bound_calc.brute_force_factor(N)
        actual_sum = p + q
        lower_bound = 2 * math.sqrt(N)

        start_time = time.perf_counter()
        bound, c_used = bound_calc.auto_bound(N=N)
        calc_time = (time.perf_counter() - start_time) * 1000

        print(f" -> Actual Factors: p = {p}, q = {q} (Actual Sum = {actual_sum})")
        print(f" -> Mathematical Floor (2*sqrt(N)): {lower_bound:.2f}")
        print(f" -> Bound (auto c={c_used}): sqrt(N) + N/{c_used} = {bound:.2f}")
        print(f" -> Calculation Time: {calc_time:.4f} ms")

        assert lower_bound <= actual_sum < bound, "CRITICAL ERROR: Bound violation detected!"
        print(" -> Status: Bound Verified Valid ✅")

    print("\n" + "=" * 80)
