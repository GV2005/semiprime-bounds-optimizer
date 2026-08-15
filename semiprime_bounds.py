import math
import time
from typing import Tuple, Union, Optional

class SemiprimeBoundsOptimizer:
    """
    Implements the piecewise static upper bounding algorithm for odd semiprimes
    as formulated by Giri Venkatesh (2026).
    
    The algorithm establishes a variable-independent algebraic ceiling for the 
    sum of prime factors (p + q) using only the value of N.
    """
    
    def __init__(self) -> None:
        # Define the exceptional coordinate pairs for the Ω set
        self.omega_set = {
            (11, 13), (11, 17), (11, 19), (11, 23), (13, 17)
        }

    def compute_bounds(self, N: int) -> Tuple[float, float, str]:
        """
        Calculates the strict lower and upper bounds of the prime factor sum (p + q)
        using only the value of N via piecewise evaluation.
        """
        if N % 2 == 0:
            raise ValueError("N must be an odd semiprime.")

        # Hard mathematical floor
        lower_bound = 2 * math.sqrt(N)
        
        # 1. Check for small prime branch inclusion using N-only modular checks
        # This determines the branch path without requiring full factorization
        p_factor: Optional[int] = None
        for p in [3, 5, 7, 11, 13]:
            if N % p == 0:
                p_factor = p
                break
                
        # 2. Evaluate Piecewise Branches
        if p_factor in {3, 5, 7}:
            upper_bound = (N / 3) + 3
            branch = f"Branch 2: Small Prime Detected (p={p_factor})"
            
        elif p_factor in {11, 13}:
            q_factor = N // p_factor
            # Check if the pair belongs to the Ω exception set
            if (p_factor, q_factor) in self.omega_set or (q_factor, p_factor) in self.omega_set:
                upper_bound = (N / 3) + 3
                branch = f"Branch 3: Exception Pair Ω Detected ({p_factor}, {q_factor})"
            else:
                upper_bound = N / 7.5625
                branch = "Branch 4: Otherwise (Bypassed Exception Pairs)"
                
        else:
            # Case where modular tests confirm p >= 17 blindly
            upper_bound = N / 7.5625
            branch = "Branch 1: Blind General Bound (p >= 17 Verified)"
            
        return lower_bound, upper_bound, branch

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
        
        # Measure calculation time of the theorem bounds
        start_time = time.perf_counter()
        low, high, branch_used = optimizer.compute_bounds(N)
        calc_time = (time.perf_counter() - start_time) * 1000
        
        # Verify against actual factorization
        p, q = optimizer.brute_force_factor(N)
        actual_sum = p + q
        
        # Calculate search window reduction against the classical baseline (N/3 + 3)
        classical_max = (N / 3) + 3
        search_reduction = 0.0 if "Branch 2" in branch_used or "Branch 3" in branch_used else 60.33
        
        print(f" -> Path Taken: {branch_used}")
        print(f" -> Actual Factors: p = {p}, q = {q} (Actual Sum = {actual_sum})")
        print(f" -> Mathematical Guarantee: {low:.2f} < (p+q) < {high:.2f}")
        print(f" -> Classic Window Maximum: {classical_max:.2f}")
        print(f" -> Active Upper Bound Compression: {search_reduction}% reduction")
        print(f" -> Calculation Complexity Speed: {calc_time:.4f} ms")
        
        # Sanity Check Assertion
        assert low <= actual_sum <= high, "CRITICAL ERROR: Boundary violation detected!"
        print(" -> Status: Bounds Verified Valid ✅")
        
    print("\n" + "=" * 80)
