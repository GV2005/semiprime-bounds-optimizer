# Semiprime Bounds Optimizer

An implementation of a piecewise static upper bounding framework for the factor sum ($p + q$) of odd semiprimes using only the value of $N$, eliminating dynamic factor dependency.

## Theoretical Background
Developed as an independent research exploration by **Giri Venkatesh (B.Tech AI & Data Science, 2026)**. This framework systematically maps small prime anomalies ($p < 17$) into distinct algebraic branches. For the generalized branch where $p \ge 17$, the algorithm applies a static coefficient bound:

$$\text{Upper Bound} = \frac{N}{7.5625}$$

This provides a **~60.33% reduction** in the leading-order search interval relative to the classical baseline ($\frac{N}{3} + 3$) without requiring prior knowledge of the underlying prime factors.

## Features
- **$N$-Only Input Dependency:** No requirement for partial or full prime factorization variables.
- **Constant Execution Complexity:** Computes boundary windows in sub-millisecond execution times.
- **Airtight Exception Bracketing:** Covers 100% of odd semiprime edge cases natively.
