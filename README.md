# Semiprime Bounds Optimizer

An implementation of a piecewise static upper bounding framework for the factor sum ($p + q$) of odd semiprimes using only the value of $N$, eliminating dynamic factor dependency.

## Theoretical Background
Developed as an independent research exploration by **Giri Venkatesh (B.Tech AI & Data Science, 2026)**. This framework systematically maps small prime anomalies ($p < 17$) into distinct algebraic branches. For the generalized branch where $p \ge 17$, the algorithm applies a static coefficient bound:

$$\text{Upper Bound} = \frac{N}{7.5625}$$

This provides a **~60.33% reduction** in the leading-order search interval relative to the classical baseline ($\frac{N}{3} + 3$) without requiring prior knowledge of the underlying prime factors.

## Generalized Parameterized Bound
The $N/7.5625$ constant above is a fixed special case of a more general, parameterized theorem:

$$S = p + q < \sqrt{N} + \frac{N}{c}$$

which holds whenever the smaller factor satisfies $p > c$. The $7.5625$ constant corresponds to a specific choice of $c$; the general form allows the bound to be tuned per-$N$ rather than fixed.

**Signature instance ($c = 20$):** if $N$ passes seven divisibility checks ($3, 5, 7, 11, 13, 17, 19 \nmid N$), then $p \ge 23 > 20$, and the bound holds.

Verified computationally across hundreds of thousands of random odd semiprimes with zero violations. Full proof available for the general parameterized form (in progress toward JRMS/arXiv publication — see `PROOF.md`).

## Features
- **$N$-Only Input Dependency:** No requirement for partial or full prime factorization variables.
- **Constant Execution Complexity:** Computes boundary windows in sub-millisecond execution times.
- **Airtight Exception Bracketing:** Covers 100% of odd semiprime edge cases natively.
- **Tunable Generalized Bound:** Supports arbitrary threshold $c$ via divisibility-based verification (`verify_c_threshold`), not just the fixed $7.5625$ constant.

## Status
- Original $N/7.5625$ bound: proven, implemented, benchmarked.
- Generalized $\sqrt{N} + N/c$ bound: proven for the general parameterized form, implemented, verified computationally with zero violations across large-scale random trials.
- Publication tracks: JRMS submission in progress; arXiv preprint (math.NT) prepared, pending endorsement.

Feedback, counterexamples, and related references are welcome via Issues.
