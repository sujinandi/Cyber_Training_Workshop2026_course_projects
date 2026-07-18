from ase.io import read
import math
import re
from ase.neighborlist import neighbor_list
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

font_path = '/home/dal941544/Arial_font/ARIAL.TTF'
prop = fm.FontProperties(fname=font_path, size=20)
tick_prop = fm.FontProperties(fname=font_path, size=16)
legend_prop = fm.FontProperties(fname=font_path, size=14)
font_name = prop.get_name()
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = font_name

au_to_fs = 0.02418884254

#Statistics on products
ch3 = []
ch2_1 = []
ch2_2 = []
ch = []
for i in range(1,33):
    ch3_cnt = 0
    ch2_1_cnt = 0
    ch2_2_cnt = 0
    ch_cnt = 0
    with open(f'./{i}/plot/traj_class.dat','r') as f :
         lines = f.readlines()
    for line in lines:
        if line.split()[1] == 'ch3':
            ch3_cnt += 1
        elif line.split()[1] == 'ch2_1':
            ch2_1_cnt += 1
        elif line.split()[1] == 'ch2_2':
            ch2_2_cnt += 1
        elif line.split()[1] == 'ch':
            ch_cnt += 1
    ch3.append(ch3_cnt)
    ch2_1.append(ch2_1_cnt)
    ch2_2.append(ch2_2_cnt)
    ch.append(ch_cnt)

data = {'CH$_3$ + H': ch3, 'CH$_2$ + H$_2$': ch2_1, 'CH$_2$ + 2H': ch2_2, 'CH + H$_2$ + H': ch}
x = np.arange(1,len(ch3)+1)
bottom = np.zeros(len(ch3))
color = ['#5DCAA5','#85B7EB','#F0997B','#AFA9EC']
plt.figure(figsize=(10, 5))

for i, (label, values) in enumerate(data.items()):
    plt.bar(x, values, bottom=bottom, color=color[i], label=label)
    bottom += np.array(values)

plt.xlabel('Initial conditions',fontsize=20, fontproperties=prop)
plt.ylabel('Number of products',fontsize=20, fontproperties=prop)
plt.ylim([0,9])
plt.xticks(x[::4], x[::4], fontproperties=prop)
plt.yticks(fontproperties=prop)
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), ncol=1, prop=legend_prop)
plt.tight_layout()
plt.savefig('./stat_products.png')

#Products and states
ch3_is = []
ch2_1_is = []
ch2_2_is = []
ch_is = []

for i in range(1,33):
    labels = []
    cls = []
    with open(f'./{i}/plot/traj_class.dat','r') as f:
        lines = f.readlines()
    for line in lines:
        labels.append(line.split()[0])
        cls.append(line.split()[1])
    mapping = dict(zip(labels, cls))

    for lb in labels:
        with open(f'./{i}/plot/E_{lb}.dat','r') as f:
            lines = f.readlines()
        match = re.search(r'istate=(\d+)', lines[0])
        if match:
            istate = int(match.group(1))
        if mapping[lb] == 'ch3':
            ch3_is.append(istate)
        elif mapping[lb] == 'ch2_1':
            ch2_1_is.append(istate)
        elif mapping[lb] == 'ch2_2':
            ch2_2_is.append(istate)
        elif mapping[lb] == 'ch':
            ch_is.append(istate)

g_num = []
g_num.append(ch3_is.count(0))
g_num.append(ch2_1_is.count(0))
g_num.append(ch2_2_is.count(0))
g_num.append(ch_is.count(0))

e_num = []
e_num.append(ch3_is.count(1))
e_num.append(ch2_1_is.count(1))
e_num.append(ch2_2_is.count(1))
e_num.append(ch_is.count(1))

plt.clf()
X = [r'CH$_3$ + H',r'CH$_2$ + H$_2$', r'CH$_2$ + 2H', r'CH + H + H$_2$']
X_axis = [1,2,3,4]
X_axis = np.array(X_axis)
colors = ["#5DCAA5", "#85B7EB", "#F0997B", "#AFA9EC"]
plt.bar(X_axis - 0.175, g_num, 0.3, color=colors, edgecolor='black')
plt.bar(X_axis + 0.175, e_num, 0.3, color=colors, edgecolor='black', hatch='//')

sim_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black',
                           label=r'S$_0$')

exp_patch = mpatches.Patch(facecolor='lightgray', edgecolor='black',
                           hatch='//', label=r'S$_1$')
plt.legend(handles=[sim_patch, exp_patch],loc='best', prop=tick_prop)

plt.xticks(X_axis, X)
plt.xlim((0.5,4.5))

plt.xlabel('Products',fontsize=20, fontproperties=prop)
plt.ylabel('Number of cases',fontsize=20, fontproperties=prop)
plt.xticks(fontproperties=prop)
plt.yticks(fontproperties=prop)
plt.tight_layout()
plt.savefig('./products_state.png')
