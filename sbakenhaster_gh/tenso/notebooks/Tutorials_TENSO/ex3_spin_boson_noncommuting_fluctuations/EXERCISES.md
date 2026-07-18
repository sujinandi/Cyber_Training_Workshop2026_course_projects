# Exercise 3: two competing environments

The un-driven spin-boson is modified to couple **two identical baths** through non-commuting operators: `bath_op1` shakes the energy levels (diagonal), `bath_op2` shakes the coupling between them (off-diagonal). Non-commuting fluctuations lead to complex dynamics that are very difficult for many quantum dynamics methods — but HEOM can address them.

## 3.1 — Run it

Run `example3.py`, then `example3_plot.py`. This is a longer calculation — you may want to set `end_time = 200`. How do the population dynamics compare with the single-bath case of Example 1?

## 3.2 — One at a time

Run with coupling given by only `bath_op1`, then only `bath_op2`, by modifying the `sys_ops` and `bath_correlations` lists in the call to `system_multibath`. Compare the population and coherence dynamics which result. Which environment moves population faster? Why?
