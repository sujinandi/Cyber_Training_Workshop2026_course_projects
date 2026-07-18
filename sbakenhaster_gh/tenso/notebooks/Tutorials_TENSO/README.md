# Tutorials_TENSO

# For a local clean installation Follow the instructions in our website:

https://ifgroup.github.io/pytenso/

# Running TENSO in Jupyter on the OOD (Open OnDemand)

This guide sets up a dedicated Jupyter kernel for the TENSO package on UB's CCR cluster,
so that the "Python (tenso)" kernel appears in any Jupyter session launched through Open OnDemand.
Everything here is **one-time setup** — once done, the kernel persists across sessions.

Adapted from the Libra kernel setup guide (`04-tsh.md`, compchem-cybertraining).

> Note: Replace `<username>` throughout this guide with your actual CCR user name,
> e.g. `jbetancourt`. You can check it with `whoami`.

---

# 1. One-time setup

## 1.1. Get access to conda

Add this to your `.bashrc` (gives access to the shared conda installation via the module system):

```bash
module use /projects/academic/cyberwksp21/MODULES
module load libra_ava/devel
```

Restart your terminal or reload your `.bashrc`:

```bash
source ~/.bashrc
```

## 1.2. Create the tenso environment and install TENSO

```bash
conda create --name tenso python=3 matplotlib
conda activate tenso
```

Clone the pytenso repository (pick a stable location — the editable install below will
point at this clone, so **do not move or delete it afterwards**):

```bash
git clone https://github.com/ifgroup/pytenso.git
cd pytenso
python -m pip install -e .
```

Quick sanity check:

```bash
python -c "from tenso.prototypes.heom import system_multibath; print('ok')"
```

> Note: The environment is created in your user space at
> `/user/<username>/.conda/envs/tenso` (the shared conda location under
> `/projects/academic/cyberwksp21/SOFTWARE/Conda` is read-only). Confirm the exact
> path with `conda env list` and `which python` — you will need it in step 1.5.

## 1.3. Register the Jupyter kernel

```bash
conda activate tenso
python -m pip install ipykernel
python -m ipykernel install --user --name tenso --display-name "Python (tenso)"
```

This creates the kernel spec at:

```
/user/<username>/.local/share/jupyter/kernels/tenso/
```

## 1.4. Replace `kernel.json`

Jupyter launched from OOD does **not** inherit your `.bashrc` environment, so the kernel
must build its own environment at startup. We do this by routing the kernel through a
launcher script.

Edit `/user/<username>/.local/share/jupyter/kernels/tenso/kernel.json` to be:

```json
{
 "argv": [
  "/user/<username>/.local/share/jupyter/kernels/tenso/launcher.sh",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python (tenso)",
 "language": "python",
 "metadata": {
  "debugger": true
 }
}
```

## 1.5. Create `launcher.sh`

Create `/user/<username>/.local/share/jupyter/kernels/tenso/launcher.sh` with the
following content:

```bash
#!/bin/bash
# ======================================================
# HARD CLEAN (CRITICAL on CCR)
# ======================================================
unset PYTHONPATH
unset PYTHONHOME
unset EBPYTHONPREFIXES
# Prevent user site leakage
export PYTHONNOUSERSITE=1
# ======================================================
# Load module environment (provides conda)
# ======================================================
module use /projects/academic/cyberwksp21/MODULES
module load libra_ava/devel
# ======================================================
# Optional: LaTeX for matplotlib text.usetex figures
# (uncomment if a texlive module is available; check with
#  `module spider texlive`)
# ======================================================
# module load texlive
# ======================================================
# Activate the tenso conda environment
# ======================================================
source /projects/academic/cyberwksp21/SOFTWARE/Conda/etc/profile.d/conda.sh
conda activate tenso
# ======================================================
# Launch kernel
# ======================================================
exec /user/<username>/.conda/envs/tenso/bin/python \
     -m ipykernel_launcher "$@"
```

Make it executable:

```bash
chmod +x /user/<username>/.local/share/jupyter/kernels/tenso/launcher.sh
```

> Note: Unlike the Libra kernel, no `LD_LIBRARY_PATH` export is needed — pytenso is
> pure Python and has no compiled shared libraries to locate.

## 1.6. Launch and test

1. Start the Jupyter app on OOD (no extra modules needed in the OOD form).
2. Select the **"Python (tenso)"** kernel.
3. Test in a cell:

```python
from tenso.prototypes.heom import system_multibath
```

---

# 2. Everyday usage

After the one-time setup, the routine is simply:

1. Launch the Jupyter app on OOD.
2. Open your notebook — Jupyter remembers the kernel per notebook, so
   "Python (tenso)" is usually already selected.

The launcher script runs automatically every time the kernel starts.

## 2.1. Adding packages

```bash
conda activate tenso
pip install <package>       # or conda install
```

Then restart the kernel in Jupyter. No changes to the kernel spec are needed.

## 2.2. Updating TENSO

Because TENSO is installed in editable mode (`pip install -e .`), any changes to the
source files in your `pytenso` clone take effect automatically on the next kernel
restart — no reinstall needed.

---

# 3. Notebooks outside your home directory

Jupyter on OOD can only "see" your home directory. If you keep notebooks elsewhere,
e.g. under `/projects/academic/cyberwksp21/Students/<your folder>`, create a symlink:

```bash
cd
ln -s /projects/academic/cyberwksp21/Students/<your folder> workshop
```

> **WARNING:** The link behaves like the real folder. `rm -r workshop` would delete
> the actual target directory. To remove only the link, use `rm workshop` (no `-r`!).

This only matters for browsing/running notebooks — Python imports (like the editable
TENSO install) work regardless of where the clone lives.

---

# 4. Troubleshooting

## 4.1. LaTeX errors in matplotlib

If figures fail with something like
`RuntimeError: Failed to process string with tex because latex could not be found`,
the code is using `text.usetex = True` but the kernel has no LaTeX on its PATH.

**Option A (easiest):** use matplotlib's built-in mathtext renderer instead:

```python
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = False
```

Math in labels (e.g. `r'$\tilde{g}/\omega_c$'`) still renders fine.

**Option B (real LaTeX):** find and load a texlive module in `launcher.sh`:

```bash
module spider texlive        # find the exact module name/version
```

Then uncomment/adjust the `module load texlive` line in `launcher.sh` and restart
the kernel.

**Option C (conda fallback):** `conda install -c conda-forge texlive-core` inside the
tenso env — but this distribution is minimal and may miss packages matplotlib wants
(e.g. `type1cm`); prefer the cluster module if one exists.

## 4.2. Kernel dies on startup

- Check the launcher is executable: `ls -l ~/.local/share/jupyter/kernels/tenso/launcher.sh`
- Check the python path at the bottom of `launcher.sh` matches `which python`
  inside the activated tenso env.
- If CCR removes or renames the `libra_ava/devel` module, edit `launcher.sh` to load
  whatever module now provides conda — or drop the two `module` lines entirely; the
  `source .../conda.sh` + `conda activate tenso` pair is usually sufficient for a
  pure-Python environment.

## 4.3. Import errors after moving files

The editable install points at the original `pytenso` clone location. If you moved it,
either move it back or reinstall from the new location:

```bash
conda activate tenso
cd /new/path/to/pytenso
python -m pip install -e .
```
