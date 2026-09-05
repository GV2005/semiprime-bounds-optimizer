# Proof Sketch & Verification Notes

## Theorem
For an odd semiprime $N = pq$ with $p \le q$, if the smaller factor satisfies $p > c$ for some chosen threshold $c$, then:

$$S = p + q < \sqrt{N} + \frac{N}{c}$$

## Establishing $p > c$ without factoring
Since $N$ is composite, $p$ must divide $N$. If none of the primes $\le c$ divide $N$, then $p$ (the smallest prime factor of $N$) cannot be one of those primes, and — since $p$ is prime — the next candidate value for $p$ is the smallest prime greater than $c$. This gives $p > c$ using only divisibility checks on $N$, with no factoring required.

**Signature instance ($c = 20$):** checking non-divisibility by $\{3, 5, 7, 11, 13, 17, 19\}$ (seven checks) rules out every prime $\le 19$, so the smallest possible remaining prime factor is $23$, giving $p \ge 23 > 20$.

## Verification methodology
- Random odd semiprimes $N = pq$ were generated across a wide range of magnitudes.
- For each $N$, the threshold condition ($p > c$ via divisibility checks) was verified before applying the bound.
- The actual factor sum $S = p + q$ (obtained via trial-division factoring, used only for verification — not by the bound itself) was checked against the predicted bound $\sqrt{N} + N/c$.
- Result: **zero violations** across hundreds of thousands of trials.
- See `semiprime_bound.py` → `compute_bound()`, `auto_bound()`, and `verify_c_threshold()` for the reference implementation used in this verification.

## Status
Full formal proof of the parameterized theorem: complete, prepared for submission (JRMS manuscript; arXiv preprint in math.NT pending endorsement). This file is a working summary for the repository — see the full paper for the complete derivation and edge-case handling.

---
*Giri Venkatesh, 2026 — independent research.*
