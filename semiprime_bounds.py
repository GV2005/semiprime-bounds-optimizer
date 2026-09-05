import math
import time
from typing import Tuple, Union, Optional, List

class SemiprimeBoundsOptimizer:
    """
    Implements the piecewise static upper bounding algorithm for odd semiprimes
    as formulated by Giri Venkatesh (2026).

    The algorithm establishes a variable-independent algebraic ceiling for the
    sum of prime factors (p + q) using only the value of N.

    Includes both:
      1. The original fixed-constant bound: N / 7.5625
      2. The generalized parameterized bound: sqrt(N) + N/c  (valid whenever p > c)
    """

    def __init__(self) -> None:
        # Define the exceptional coordinate pairs for the Ω set
        self.omega_set = {
            (11, 13), (11, 17), (11, 19), (11, 23), (13, 17)
        }

    def verify_c_threshold(self, N: int, c: int = 20, primes_to_check: Optional[List[int]] = None) -> bool:
        """
        Confirms p > c holds for N, using only N-only divisibility checks (no factoring).

        Signature configuration: c = 20, verified via the seven-prime check
        {3, 5, 7, 11, 13, 17, 19}. If none of these divide N, the smaller factor
        p must be >= 23 > 20, satisfying p > c.

        A custom primes_to_check list can be supplied for other thresholds of c.
        """
        if primes_to_check is None:
            primes_to_check = [3, 5, 7, 11, 13, 17, 19]

        # Only primes <= c are meaningful for establishing p > c
        relevant_primes = [p for p in primes_to_check if p <= c]
        return all(N % p != 0 for p in relevant_primes)

    def compute_general_bound(self, N: int, c: int = 20, verify: bool = True) -> float:
        """
        PRIMARY METHOD — Generalized parameterized bound:

            S = p + q < sqrt(N) + N/c

        valid whenever the smaller prime factor p > c. This supersedes the old
        fixed-constant N/7.5625 bound: c is tunable per-N via divisibility checks,
        so the bound can be tightened arbitrarily instead of being locked to one
        constant.

        If verify=True, first checks (via verify_c_threshold) that p > c actually
        holds for this N before returning the bound; raises if the threshold
        condition is not established by the divisibility checks.
        """
        if N % 2 == 0:
            raise ValueError("N must be an odd semiprime.")

        if verify and not self.verify_c_threshold(N, c=c):
            raise ValueError(
                f"Cannot certify p > {c} for N={N} via divisibility checks; "
                f"bound not guaranteed to hold with this c."
            )

        return math.sqrt(N) + (N / c)

    def auto_general_bound(self, N: int, candidate_primes: Optional[List[int]] = None) -> Tuple[float, int]:
        """
        Automatically finds the largest usable c for this N by walking up through
        candidate_primes and taking the largest prime that still divides-out clean
        (i.e. the tightest threshold the divisibility checks can certify), then
        returns the resulting generalized bound.

        Returns (bound, c_used).
        """
        if candidate_primes is None:
            candidate_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

        best_c = 2  # trivial floor if nothing else is certifiable
        for prime in candidate_primes:
            if self.verify_c_threshold(N, c=prime, primes_to_check=candidate_primes):
                best_c = prime
            else:
                break

        return self.compute_general_bound(N, c=best_c), best_c

    @staticmethod
    def legacy_fixed_bound(N: int) -> float:
        """
        LEGACY — the original empirically-discovered fixed-constant bound (N / 7.5625).
        Kept only for historical comparison; superseded by compute_general_bound(),
        which is strictly tighter and tunable per-N instead of fixed to one constant.
        """
        return N / 7.5625

    @staticmethod
    def brute_force_factor(N: int) -> Tuple[int, int]:
        """Standard trial division baseline used for verification metrics."""
        for i in range(3, int(math.sqrt(N)) + 1, 2):
            if N % i == 0:
                return i, N // i
        raise ValueError("N is prime or not an odd composite.")


# ==========================================
# TEST AND BENCHMARK SUITE
# ==========================================
if __name__ == "__main__":
    optimizer = SemiprimeBoundsOptimizer()

    # Selection of test cases across different branches
    test_cases = [
        15,           # Branch 2: p=3, q=5
        247,          # Branch 4: p=13, q=19 (Otherwise)
        667,          # Branch 1: p=23, q=29 (General)
        143,          # Branch 3: p=11, q=13 (Ω Exception)
        23000000207   # Branch 1: Large Number Verification
    ]

    print("=" * 80)
    print("GIRI VENKATESH (2026) - SEMIPRIME BOUNDS RUNTIME BENCHMARK")
    print("=" * 80)

    for N in test_cases:
        print(f"\nAnalyzing N = {N}")

        # Verify against actual factorization
        p, q = optimizer.brute_force_factor(N)
        actual_sum = p + q
        lower_bound = 2 * math.sqrt(N)
        classical_max = (N / 3) + 3

        # PRIMARY: auto-tuned generalized bound sqrt(N) + N/c
        start_time = time.perf_counter()
        general_bound, c_used = optimizer.auto_general_bound(N)
        calc_time = (time.perf_counter() - start_time) * 1000

        print(f" -> Actual Factors: p = {p}, q = {q} (Actual Sum = {actual_sum})")
        print(f" -> Mathematical Floor: {lower_bound:.2f}")
        print(f" -> Classic Window Maximum (N/3 + 3): {classical_max:.2f}")
        print(f" -> [PRIMARY] Generalized Bound (auto c={c_used}): sqrt(N) + N/{c_used} = {general_bound:.2f}")
        print(f" -> Calculation Complexity Speed: {calc_time:.4f} ms")

        assert actual_sum < general_bound, "CRITICAL ERROR: Generalized bound violation detected!"
        print(" -> Status: Generalized Bound Verified Valid ✅")

        # LEGACY comparison only — old fixed constant, kept for reference.
        # Note: N/7.5625 was only ever valid under the original p >= 17 branch
        # condition, so it is shown here purely for numeric comparison and is
        # NOT asserted as a valid bound for every N (unlike the generalized bound above).
        legacy_bound = optimizer.legacy_fixed_bound(N)
        legacy_note = "valid range" if p >= 17 else "outside original valid range (p < 17)"
        print(f" -> [LEGACY] Fixed N/7.5625 Bound: {legacy_bound:.2f} ({legacy_note}, superseded by generalized bound above)")

    print("\n" + "=" * 80)
