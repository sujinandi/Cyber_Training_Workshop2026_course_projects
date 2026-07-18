from ase.io import read
import math
from ase.neighborlist import neighbor_list
import numpy as np
import matplotlib.pyplot as plt

au_to_fs = 0.02418884254
def parse_trajectory_with_temperature(xyz_filename):
    # 1. Read all frames in the file using index=':'
    # This returns a list of ASE Atoms objects
    trajectory = read(xyz_filename, index=':')
    
    times = []
    
    # 2. Loop through each frame and extract 'T'
    for index, atoms in enumerate(trajectory):
        # In ASE 3.17.0, parsed comment-line properties live in atoms.info
        T_value = atoms.info.get('T')
        # Fallback check in case a frame is missing the T metadata
        if T_value is not None:
            times.append(math.ceil(float(T_value)*au_to_fs*10.0) / 10.0)
        else:
            print("Warning: Frame {} is missing 'T' in its comment line!".format(index))
            times.append(None)
    times = np.array(times)

    return trajectory, times

def class_result(atoms_list, cutoff = 3.0):
    class_arr = []
    for atoms in atoms_list:
        c_h_idx = []                    
        i, j, d = neighbor_list('ijd', atoms, cutoff)
        
        ch_count = 0
        for idx_a, idx_b in zip(i, j):
            # Avoid double counting (i > j) and check elements
            if idx_a < idx_b:
                symbols = [atoms[idx_a].symbol, atoms[idx_b].symbol]
                if 'C' in symbols and 'H' in symbols:
                    ch_count += 1
                    if atoms[idx_a].symbol == 'H':
                        c_h_idx.append(idx_a)
                    if atoms[idx_b].symbol == 'H':
                        c_h_idx.append(idx_b)
        hh_idx = []
        for a_i in range(len(atoms)):
            if atoms[a_i].symbol == 'H' and a_i not in c_h_idx:
                hh_idx.append(a_i)
        h2 = False
        if ch_count == 2:
            h2 = any(hh in i for hh in hh_idx)   # exactly one decision per frame
            class_arr.append('ch2_1') if h2 else class_arr.append('ch2_2')
        elif ch_count == 3:
            class_arr.append('ch3')
        elif ch_count == 1:
            class_arr.append('ch')
        elif ch_count == 4:
            class_arr.append('ch4')

    class_arr = np.array(class_arr)

    return class_arr
# ==========================================
# Example Usage:
# ==========================================
if __name__ == "__main__":
    colors = ["r", "g", "b", "m", "y", "c", "k", "gray", "indigo", "fuchsia", "lime", "darkred", "gold", 
    "olive", "cyan", "teal", "orange", "limegreen", "firebrick", "olive"]

    # Replace 'geom.xyz' with your actual file path
    labels = []
    ref_times = np.arange(0,50.01,0.1)
    ref_times = np.round(ref_times, 1)
    ch4_arr = np.zeros(len(ref_times))
    ch3_arr = np.zeros(len(ref_times))
    ch2_1_arr = np.zeros(len(ref_times))
    ch2_2_arr = np.zeros(len(ref_times))
    ch_arr = np.zeros(len(ref_times))

    with open('Labels.dat','r') as f:
        lines = f.readlines()
    for line in lines:
        labels.append(line.split()[0])
    
    for lb in labels:
        xyz_file = f'traj_{lb}.xyz' 
    
        atoms_traj, t_array = parse_trajectory_with_temperature(xyz_file)
        class_array = class_result(atoms_traj)
        with open('traj_class.dat','a') as f:
            f.write(f'{lb} {class_array[-1]}\n')

        pop_file = f'{lb}_pop.dat'
        with open(pop_file, 'r') as f:
            lines = f.readlines()
        pop_t = []
        pop_val = []
        for line in lines:
            parts = line.split()
            pop_t.append(float(parts[0]))
            pop_val.append(float(parts[1]))
        
        pop_t = np.array(pop_t)
        pop_val = np.array(pop_val)
        pop_t_rounded = np.round(pop_t, 1)
        
        pop_map = dict(zip(pop_t_rounded, pop_val))
        
        map_arr = {}
        for t, y in zip(t_array, class_array):
            if t in pop_map:
                map_arr[t] = (y, pop_map[t])

        tmp_ch4_arr = []
        tmp_ch3_arr = []
        tmp_ch2_1_arr = []
        tmp_ch2_2_arr = []
        tmp_ch_arr = []
        for t in ref_times:
            current_ch4 = 0.0
            current_ch3 = 0.0
            current_ch2_1 = 0.0
            current_ch2_2 = 0.0
            current_ch = 0.0

            if t in map_arr:
                y_val, z_val = map_arr[t]
                if y_val == 'ch4': current_ch4 += z_val
                elif y_val == 'ch3': current_ch3 += z_val
                elif y_val == 'ch2_1': current_ch2_1 += z_val
                elif y_val == 'ch2_2': current_ch2_2 += z_val
                elif y_val == 'ch': current_ch += z_val
            tmp_ch4_arr.append(current_ch4)
            tmp_ch3_arr.append(current_ch3)
            tmp_ch2_1_arr.append(current_ch2_1)
            tmp_ch2_2_arr.append(current_ch2_2)        
            tmp_ch_arr.append(current_ch)        
        ch4_arr = ch4_arr + np.array(tmp_ch4_arr)
        ch3_arr = ch3_arr + np.array(tmp_ch3_arr)
        ch2_1_arr = ch2_1_arr + np.array(tmp_ch2_1_arr)
        ch2_2_arr = ch2_2_arr + np.array(tmp_ch2_2_arr)
        ch_arr = ch_arr + np.array(tmp_ch_arr)
    with open('product_pop.dat','a') as f:
        for i in range(len(ref_times)):
            f.write(f'{ref_times[i]} {ch4_arr[i]} {ch3_arr[i]} {ch2_1_arr[i]} {ch2_2_arr[i]} {ch_arr[i]}\n')

    plt.plot(ref_times, ch4_arr, label='CH$_4$')
    plt.plot(ref_times, ch3_arr, label='CH$_3$ + H')
    plt.plot(ref_times, ch2_1_arr, label='CH$_2$ + H$_2$')
    plt.plot(ref_times, ch2_2_arr, label='CH$_2$ + 2H')
    plt.plot(ref_times, ch_arr, label='CH + H$_2$ + H')
    
    plt.xlabel('Time (fs)')
    plt.ylabel('Population')

    plt.legend(loc='best', ncol=1)
    plt.tight_layout()
    plt.savefig('./product_pop.png')

