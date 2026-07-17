# Vibronic Coherence Across Nonadiabatic Dynamics Methods
### Victor M. Freixas — CyberTraining 2026 project

A machine-learned quasi-diabatic Hamiltonian (NQDH, HIP-NN based) for a
122-atom halofluorescein heterodimer drives five nonadiabatic dynamics
methods through one diabatic interface: our reference Ehrenfest
integrator, FSSH / SHXF / QTSH through Libra, and full multiple spawning
through pySpawn, at 300-initial-condition ensemble scale.

- **Report (PDF):** [report.pdf](report.pdf)
- **Full project repository** (code, frozen model, initial conditions,
  per-figure data and plotting scripts):
  https://github.com/vmfreixas/nqdh-beating-demo

Main finding: the survival of the S1/S2 vibronic beat is decided by the
per-trajectory energy gate at surface-transfer events (surface-hopping
family) and by the spawned-basis size (FMS, which recovers the beat as
the basis converges).
