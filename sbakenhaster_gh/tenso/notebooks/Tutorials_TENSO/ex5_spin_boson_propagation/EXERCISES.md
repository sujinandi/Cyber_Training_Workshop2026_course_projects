# Exercise 5: time propagation algorithms

Same physics, same tensor network — different integrators, selected with `stepwise_method='simple'` plus the `ps_method` argument: `'vmf'` directly integrates one coupled master equation for all core tensors; `'ps1'` (projector splitting) sweeps through the network one tensor at a time. Both are fixed-rank methods.

## 5.1 — Do they agree?

Run `example5.py`, then `example5_plot.py` — the `ps1` and `vmf` curves should coincide. Load both output files and print the max difference. Note the it/s from the progress bars: which scheme is faster?

## 5.2 — A third scheme

Add `'ps2'` to `ps_methods`. PS2 is like PS1 but adaptively grows the tensor sizes mid-run. Does it agree, and how does its speed compare? (You may not want to run this one to the end.)

## 5.3 — The default strategy (optional)

Drop the `stepwise_method` and `ps_method` arguments to get TENSO's default `'mix'` strategy: adaptive PS2 to build up the ranks from the simple initial state, then VMF for production. How does it compare?
