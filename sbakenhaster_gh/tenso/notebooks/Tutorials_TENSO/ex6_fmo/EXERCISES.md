# Exercise 6: the 3-site FMO complex

The Fenna-Matthews-Olson (FMO) complex is a piece of photosynthetic machinery in bacteria and a common quantum dynamics benchmark. Here we treat the {|0⟩, |1⟩, |2⟩} 3-site subsystem, with a separate bath coupled to each site.

⚠️ `example6.py` also contains configurations with structured spectral densities — those calculations take many hours, more time than we have; they are provided for reference. Stick to the Drude-Lorentz bath below.

## 6.1 — Build the input

Create a TENSO input for the 3-site FMO subsystem:

- System Hamiltonian (cm⁻¹): the 3×3 matrix `H` in `example6.py`.
- Coupling Hamiltonians: one projector per site, coupled to three equivalent Drude-Lorentz baths (`re_d=[35]`, `width_d=[106.2]`), one per site — that is, `sys_ops` holds the three site projectors and `bath_correlations` holds three copies of the same bath.
- Initial state: the excitation starts on site 1.

Monitor the site populations up to 1 ps. Where does the excitation end up?

(You can write the input from scratch following the pattern of the earlier examples, or strip `example6.py` down to a single Drude configuration and compare.)

## 6.2 — Low-temperature corrections

How many low-temperature correction terms (`n_ltc`) do you need for convergence at 300 K? What about at 77 K?
