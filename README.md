# Semiprime Factor-Sum Bound

An $N$-only upper bound on the factor sum ($p + q$) of odd semiprimes $N = pq$, requiring no factorization of $N$.

## Theorem
For an odd semiprime $N = pq$ with $p \le q$, if the smaller factor satisfies $p > c$ for a chosen threshold $c$, then:

$$S = p + q < \sqrt{N} + \frac{N}{c}$$

The threshold $c$ can be established for a given $N$ using only divisibility checks — no factoring required.

## Establishing $p > c$
If none of the primes $\le c$ divide $N$, then $N$'s smallest prime factor $p$ cannot be one of those primes, so $p$ must exceed $c$.

**Signature instance ($c = 20$):** checking non-divisibility by $\{3, 5, 7, 11, 13, 17, 19\}$ (seven checks) rules out every prime $\le 19$, so $p \ge 23 > 20$, and the bound applies with $c = 20$.

## Verification
Verified computationally across hundreds of thousands of random odd semiprimes, with the threshold condition checked before applying the bound in every case. **Zero violations.**

See `PROOF.md` for the derivation and verification methodology, and `semiprime_bound.py` for the reference implementation.

## Status
Developed by **Giri Venkatesh (B.Tech AI & Data Science, 2026)** as independent research. Publication in progress — JRMS submission prepared; arXiv preprint (math.NT) prepared, pending endorsement.

Feedback, counterexamples, and related references are welcome via Issues.
