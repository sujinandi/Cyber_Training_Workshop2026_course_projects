# Exercise 2: tensor network structures

The same spin-boson calculation runs twice, changing only the tensor-network structure through the `frame_method` argument: `'tree2'` builds a balanced binary tensor tree, `'train'` builds a tensor train (chain). The physics must not depend on this choice — only the cost can.

## 2.1 — Converged answers

Run `example2.py`, then `example2_plot.py`. Do you see any difference between the results given by the tree and the train network? Should you?

## 2.2 — Computational speed

The tqdm bar reports each run's speed (iterations/s). Which tensor-network structure is faster in this case? How large is the difference?

## 2.3 — A third structure (optional)

Add `'naive': 'naive'` to `outs`. This results in one big unfactorized tensor. How long does it take in comparison to the tree or train structures? Would it be a good idea for larger systems?
