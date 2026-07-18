# Virtual Photon Decay in Ar·H₂O — complete ab initio mechanism

**Owen Holtfrank** · Georgia Institute of Technology (Kretchmer group) ·
CyberTraining 2026 course project

---

## The result in one sentence

An Ar 3s⁻¹ hole at 28.97 eV, unable to decay by ICD (Coulomb-blocked),
transfers its energy by virtual photon to a **bright superexcited state of water
at 13.3 eV**; that state turns out to be **bound**, not directly dissociative,
so fragmentation proceeds by **internal conversion down the Rydberg–valence
manifold** onto the Ã surface, which ejects an H atom in 16.4 fs.

**This contradicts the standard Fermi-golden-rule treatment**, which assumes the
acceptor absorbs and dissociates in one step. See
[the finding](project/README.md#the-finding-fgrs-one-step-assumption-fails-here).

| | value | method |
|---|---|---|
| donor | **28.97 eV** | XMS-CASPT2 (expt. 29.24) |
| acceptor | **13.30 eV**, f = 0.157 | SA-20-CASSCF + RASSI |
| coupling | **12.37** vs **9.35 meV** | two independent routes, 30% agreement |
| acceptor is bound | **0.1%** fragmentation | classical, on the computed surface |
| cascade | **225 spawns**, 16/16 trajectories, funnel to Ã | **AIMS (PySpawn)** |
| fragmentation | **31.4%**, 16.4 fs, H at 0.60 eV | classical, on the Ã surface |

---

## Workshop software: adoption, integration, future use

**Three workshop codes, integrated into one workflow** — and the project could
not have been done with any one of them alone:

```
OpenMolcas ──> surfaces, oscillator strengths, XMS-CASPT2 validation
     │
     └──> PySpawn ──> AIMS cascade (the central result)
     │         ↑
     │         └── REQUIRED PATCHING (see below)
     │
Libra ──────> NE-FGR attempt (documented negative) + analysis environment
```

### I patched PySpawn to make this project possible

`molcas_interface.py::get_overlap` **hard-exits above 10 singlet states.** This
project needs 13. The fix was not a bigger array bound: the RASSI
`OVERLAP MATRIX FOR THE ORIGINAL STATES` block is the **lower triangle of the
combined (2N)×(2N) overlap over both geometries** — 351 floats for N=13, which
is 26·27/2 — so the original hardcoded 5/10-state line-counting cannot
generalize. Replaced with a token-based parser that slices the cross-geometry
block, **verified against a 13-state run** (diagonal reproduced to five
decimals; 16 trajectories × 2 days × 225 spawns with no issues).

→ [`project/patches/molcas_interface_get_overlap.diff`](project/patches/) · reported to B. Levine

### I found a bug in the workshop's OpenMolcas→PySpawn Hessian converter

`Molcas_2_pySpawn_hessian.py` reads the **BFGS optimizer** Hessian from
`.slapaf.h5` rather than the analytic MCKINLEY one → ~15% high frequencies →
~15% wrong Wigner amplitudes for anyone converting after a geometry
optimization. Reported to A. Mehmood. This project works around it by
reconstructing from `.freq.molden` normal modes.

### Continued use

This is not a workshop exercise that ends here. The AIMS capability goes
directly into:

- **My thesis** — the cascade result is the dynamical half of the VPD chapter.
- **A JPCL manuscript in preparation** (Ar_n·H₂O ICD/ETMD competition) — the
  fragmentation KER answers the "observable signature" question my candidacy
  committee raised.
- **A follow-up model-system study** — the two-acceptor experiment proposed in
  the project README, testing when the FGR one-step assumption fails. That study
  is designed around Libra + PySpawn.
- **An open question to A. Akimov** on whether NE-FGR supports dissociative
  continuum acceptors, arising directly from the documented negative in
  `04_rates_and_coupling/`.

---

## Repository

```
oholtfrank/
├── README.md          <- you are here
├── coursework/        <- workshop tutorials → what fed the project
└── project/           <- the VPD mechanism
    ├── README.md      <- full writeup: mechanism, rigor tiers, open items
    ├── 01_electronic_structure/    donor 28.97 eV; ICD Coulomb-blocked
    ├── 02_acceptor_identification/ state 12: resonant + bright + falling
    ├── 03_surfaces/                1D + 2D scans; the acceptor is flat/rising
    ├── 04_rates_and_coupling/      12.37 vs 9.35 meV; NE-FGR negative
    ├── 05_aims/                    the cascade — 225 spawns, funnel to Ã
    ├── 06_fragmentation/           bound acceptor (0.1%); Ã (31.4%, 16.4 fs)
    ├── 07_caspt2_validation/       13.344 eV — ordering and resonance survive
    └── patches/                    the get_overlap fix
```

**Start here:** [`project/README.md`](project/README.md) for the science,
[`coursework/README.md`](coursework/README.md) for the workshop through-line.

### Reproducing

Every figure is built from committed `.npz` files — no raw `.out` needed.
Raw AIMS trajectories (16 × `sim.hdf5`, ~295 MB) are archived separately
[Zenodo DOI: TBD]; `05_aims/results/cascade_stats.txt` holds the extracted
statistics. Environment and SLURM settings are documented in
[`coursework/README.md`](coursework/README.md#environment-notes).

## Programs used

**OpenMolcas** (SA-CASSCF, XMS-CASPT2, RASSI) · **PySpawn** (AIMS, patched) ·
**Libra** (NE-FGR, analysis env) · NumPy/SciPy/matplotlib · SLURM ·
PySCF/`pyscf_prism` (tetrazine benchmarking coursework)
