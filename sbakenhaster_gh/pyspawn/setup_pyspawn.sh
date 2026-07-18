# setup_pyspawn.sh

# CONDA_NO_PLUGINS=true \
# CONDA_SOLVER=classic \
# conda create -y -p $HOME/pyspawn python=2.7

# CONDA_NO_PLUGINS=true \
# CONDA_SOLVER=classic \ 
# conda create -y -p $HOME/pyspawn python=2.7



echo "Activating Miniforge3"
source /projects/academic/cyberwksp21/SOFTWARE_2026/miniforge3/etc/profile.d/conda.sh

CONDA_NO_PLUGINS=true \
CONDA_SOLVER=classic \
conda create -y -p $HOME/pyspawn python=2.7

echo "Creating and activating pyspawn env to: \$HOME/pyspawn"
conda create -y -p $HOME/pyspawn python=2.7
#  CONDA_NO_PLUGINS=true
conda activate $HOME/pyspawn

echo "Setting up pyspawn dependencies"
pip install numpy h5py matplotlib typing

echo "Setting up pyspawn"
git clone https://github.com/blevine37/pySpawn17
cd pySpawn17/
python setup.py install

cd ../
rm -rf pySpawn17

echo "Done."
echo "Activate with:"
echo "source /projects/academic/cyberwksp21/SOFTWARE_2026/miniforge3/etc/profile.d/conda.sh"
echo "conda activate \$HOME/pyspawn."
