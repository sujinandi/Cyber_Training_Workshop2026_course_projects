# TENSO Hands-On Tutorial: Simulating Quantum Systems in Real Environments

## What this tutorial is about

No quantum system is ever truly isolated: a molecule sits in a solvent, a qubit sits in a chip, a pigment sits in a protein. This tutorial teaches you to simulate such **open quantum systems** — a small quantum system exchanging energy and losing coherence to its surroundings — using **TENSO**, a tensor-network package for numerically exact quantum dynamics.

No background in open quantum systems is required. If you can run a Python script and have done any kind of numerical simulation (DFT, MD, ML training runs), you have all the prerequisites. The quantum-mechanics ingredients are introduced as you meet them, and every simulation input is a short, commented Python script.

## What you will learn

By the end of the tutorial you will be able to:

1. **Set up and run** an open-system simulation: define the system (a Hamiltonian matrix), the environment (a "bath" with a coupling strength and a temperature), and how they couple.
2. **Read the results**: population relaxation toward thermal equilibrium, loss of quantum coherence, and how temperature and coupling strength control both.
3. **Tell physical parameters apart from numerical ones** — and converge the numerical ones. Tensor-network structure, propagation algorithm, hierarchy depth, and time step must *not* change the answer; you will verify this yourself.
4. **Apply the machinery to real problems**: laser control of a two-level system (the physics of quantum-gate errors) and energy transfer in a photosynthetic complex (FMO).

The recurring theme — familiar from basis sets, k-points, or hyperparameters — is: *a result you have not converged is not a result.*

## Setup

You need Python with `tenso` installed, plus `numpy`, `matplotlib`, and `tqdm`. Check your installation with:

```bash
python -c "import tenso; print('ok')"
```

## How the tutorial is run

The material is six guided examples (`ex1` … `ex6`), done in order. Each folder contains:

- `exampleN.py` — a ready-to-run simulation script,
- `exampleN_plot.py` — a plotting script for the results,
- `EXERCISES.md` — 2–3 short tasks (~20–30 minutes per example).

The rhythm for each example: a short introduction by the instructor, run the baseline script, then work through the exercises (in pairs is encouraged) and discuss as a group. The exercises are of the form *change one parameter, rerun, explain what you see* — the fastest way to build intuition.

Practical tips:

- Simulations write their results to plain-text files (`<name>.dat.log`) in the folder you run from. **Rename the output before rerunning** with changed parameters, so you can compare curves.
- Progress bars show the simulation speed; none of the main-track runs should take more than a few minutes on a laptop. Runtime warnings are given where it matters.

## Program

| # | Folder | Topic | The takeaway |
|---|--------|-------|--------------|
| 1 | `ex1_spin_boson_simple` | Your first open-system simulation | The anatomy of a simulation input: system, bath, coupling, temperature. Relaxation to thermal equilibrium. |
| 2 | `ex2_spin_boson` | Tensor-network structures | The network layout (tree vs chain) is a numerical representation choice — like a basis set, it must not change the physics, only the cost. |
| 3 | `ex3_spin_boson_noncommuting_fluctuations` | Two competing environments | Multiple baths coupled through incompatible operators — a regime where approximate methods fail and exact ones earn their keep. |
| 4 | `ex4_spin_boson_time_dependent` | Driving with a laser pulse | Time-dependent control in the presence of noise: why real quantum gates aren't perfect. |
| 5 | `ex5_spin_boson_propagation` | Propagation algorithms | Different time integrators (VMF vs projector splitting), their speed/robustness trade-offs, and what the code's defaults do for you. |
| 6 | `ex6_fmo` | Energy transfer in photosynthesis | Capstone: the same machinery applied to a real 3-site pigment-protein complex — follow the excitation to the reaction center. |

## Suggested timing

| Block | Content | Time |
|-------|---------|------|
| Intro | What is an open quantum system; tour of a TENSO input | ~20 min |
| Block 1 | ex1 → ex2 → ex3: fundamentals | ~90 min |
| Break | | |
| Block 2 | ex4 → ex5 → ex6: control, algorithms, application | ~90 min |
| Wrap-up | Discussion and outlook | ~15 min |
