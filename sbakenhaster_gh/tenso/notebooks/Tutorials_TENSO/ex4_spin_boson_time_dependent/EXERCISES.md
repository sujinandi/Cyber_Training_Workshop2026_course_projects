# Exercise 4: driving the system with a laser pulse

A time-dependent field is added through the `td_f` (field) and `td_op` (light-matter coupling) arguments: a Gaussian laser pulse that hits at t ≈ 6 fs and, ideally, executes a Hadamard gate on the two-level system. The bath acts during the operation — this is the physics behind quantum control and gate errors, and decoherence is a great challenge in quantum information.

## 4.1 — Effectiveness of the pulse

Run `example4.py`, then `example4_plot.py`. Ideally the pulse should result in the execution of a Hadamard gate. Are the final populations consistent with successful execution? What about the coherences?

## 4.2 — Modifying the environmental coupling strength

Double the coupling, `re_d = [1080]`, and rerun the pulse. Then try halving the coupling strength instead. How is the performance of the gate impacted? Does modifying the strength of the Brownian feature (`re_b`) have a larger or smaller impact?
