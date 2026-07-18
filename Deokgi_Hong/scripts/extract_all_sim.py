from ase.io import read
import math
from ase.neighborlist import neighbor_list
import numpy as np
import matplotlib.pyplot as plt
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

#Electronic population
times = []
el_g_pop = []
el_e_pop = []
with open('./1/plot/N.dat','r') as f:
    lines = f.readlines()
for line in lines:
    times.append(math.ceil(float(line.split()[0])*au_to_fs*10.0) / 10.0)
    el_g_pop.append(float(line.split()[1]))
    el_e_pop.append(float(line.split()[2]))
times = np.array(times)
el_g_pop = np.array(el_g_pop)
el_e_pop = np.array(el_e_pop)

for i in range(2,33):
    tmp_times = []
    tmp_el_g_pop = []
    tmp_el_e_pop = []
    with open(f'./{i}/plot/N.dat','r') as f :
         lines = f.readlines()
    for line in lines:
        tmp_el_g_pop.append(float(line.split()[1]))
        tmp_el_e_pop.append(float(line.split()[2]))
    tmp_el_g_pop = np.array(tmp_el_g_pop)
    tmp_el_e_pop = np.array(tmp_el_e_pop)

    el_g_pop = el_g_pop + tmp_el_g_pop    
    el_e_pop = el_e_pop + tmp_el_e_pop    

el_g_pop = el_g_pop / 32 
el_e_pop = el_e_pop / 32 

plt.plot(times, el_g_pop,label='S0',color='#1F77B4')
plt.plot(times, el_e_pop,label='S1',color='#FF8213')

plt.xlabel('Time (fs)',fontsize=20, fontproperties=prop)
plt.ylabel('Population',fontsize=20, fontproperties=prop)
plt.xticks(fontproperties=prop)
plt.yticks(fontproperties=prop)
plt.legend(loc='best',ncol=1, prop=legend_prop)
plt.tight_layout()
plt.savefig('./state_population.png')

#Products ratio
ch4_pop = []
ch3_pop = []
ch2_1_pop = []
ch2_2_pop = []
ch_pop = []

with open('./1/plot/product_pop.dat','r') as f:
    lines = f.readlines()

for line in lines:
    ch4_pop.append(float(line.split()[1]))
    ch3_pop.append(float(line.split()[2]))
    ch2_1_pop.append(float(line.split()[3]))
    ch2_2_pop.append(float(line.split()[4]))
    ch_pop.append(float(line.split()[5]))

ch4_pop = np.array(ch4_pop)
ch3_pop = np.array(ch3_pop)
ch2_1_pop = np.array(ch2_1_pop)
ch2_2_pop = np.array(ch2_2_pop)
ch_pop = np.array(ch_pop)

for i in range(2,33):
    tmp_ch4_pop = []
    tmp_ch3_pop = []
    tmp_ch2_1_pop = []
    tmp_ch2_2_pop = []
    tmp_ch_pop = []

    with open(f'./{i}/plot/product_pop.dat','r') as f:
        lines = f.readlines()
    
    for line in lines:
        tmp_ch4_pop.append(float(line.split()[1]))
        tmp_ch3_pop.append(float(line.split()[2]))
        tmp_ch2_1_pop.append(float(line.split()[3]))
        tmp_ch2_2_pop.append(float(line.split()[4]))
        tmp_ch_pop.append(float(line.split()[5]))

    ch4_pop = ch4_pop + np.array(tmp_ch4_pop)
    ch3_pop = ch3_pop + np.array(tmp_ch3_pop)
    ch2_1_pop = ch2_1_pop + np.array(tmp_ch2_1_pop)
    ch2_2_pop = ch2_2_pop + np.array(tmp_ch2_2_pop)
    ch_pop = ch_pop + np.array(tmp_ch_pop)

ch4_pop = ch4_pop / 30
ch3_pop = ch3_pop / 30
ch2_1_pop = ch2_1_pop / 30
ch2_2_pop = ch2_2_pop / 30
ch_pop = ch_pop / 30

with open('fin_species_ratio.dat','a') as f:
    f.write(f'CH4: {ch4_pop[-1]}\n')
    f.write(f'CH3 + H: {ch3_pop[-1]}\n')
    f.write(f'CH2 + H2: {ch2_1_pop[-1]}\n')
    f.write(f'CH2 + 2H: {ch2_2_pop[-1]}\n')
    f.write(f'CH + H2 + H: {ch_pop[-1]}\n')

plt.clf()
plt.plot(times, ch4_pop,label=r'CH$_4$',color='black')
plt.plot(times, ch3_pop,label=r'CH$_3$ + H',color='#5DCAA5')
plt.plot(times, ch2_1_pop,label=r'CH$_2$ + H$_2$',color='#85B7EB')
plt.plot(times, ch2_2_pop,label=r'CH$_2$ + 2H',color='#F0997B')
plt.plot(times, ch_pop,label=r'CH + H$_2$ + H',color='#AFA9EC')

plt.xlabel('Time (fs)',fontsize=20, fontproperties=prop)
plt.ylabel('Ratio of species',fontsize=20, fontproperties=prop)
plt.xlim([0,50])
plt.xticks(fontproperties=prop)
plt.yticks(fontproperties=prop)
plt.legend(bbox_to_anchor = (0.,1.02, 1., 0.102), loc='lower left', mode="expand", ncol=3, frameon=True, prop=legend_prop)
plt.tight_layout()
plt.savefig('./species_population.png')
