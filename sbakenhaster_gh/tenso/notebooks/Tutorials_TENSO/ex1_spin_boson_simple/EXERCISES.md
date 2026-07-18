# Exercise 1: a minimal open-system simulation

A two-level system (TLS) sits in contact with a semi-structured environment — one Drude-Lorentz feature (e.g. solvent) plus one Brownian oscillator feature (e.g. vibrations) — and we watch the bath drag it toward thermal equilibrium. The baseline run takes 4–10 minutes depending on your hardware.

## 1.1 — Run it

Launch `example1.py`, then `example1_plot.py`. All population starts in the higher-energy state of the TLS — how long until the system reaches equilibrium?

## 1.2 — Temperature

Raise `temperature` in `gen_bcf` from 300 → 600 K — do the populations shift the way Boltzmann statistics predict?

## 1.3 — Remove the structure from the bath

Remove the Brownian feature (the `freq_b`, `re_b`, and `width_b` arguments of `gen_bcf`). What impact does this have on the dynamics and on the computational speed?

## 1.4 — Coupling strength (optional)

Weaken `re_d` from `[540]` to `[54]` (10× weaker). What is the impact on the dynamics? Are oscillations enhanced or suppressed?
