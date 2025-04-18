# generic script 
# Phonon band structure and density of states and frequencies and eigenvectors 

# Import stuffs  
import numpy as np
import csv
import pickle
from atom_position import *
import time 
import gzip


start = time.time()

#=====================
#Input part 
natom, a_1, a_2, a_3 = get_lattice('lammps.dat') 
at_id, mol_id, x, y, z = get_position('lammps.dat', natom)
print ("natom :", natom, flush=True)
#====================

# load freqs, eigvecs
# Save every eigenval and eigenvec unchanged
frequencies = pickle.load(gzip.open("freq_phonopy", "rb"))
eigvecs = pickle.load(gzip.open("eigvecs_phonopy", "rb"))
print ("Loaded the matrix")


max_freq = 30
# Till what frequecy we want to cut, at Gamma point  
print("------------------------------------")
print(f"Normalized eigenvectors within {max_freq} THz")
print ("------------------------------------")

f = open('atom_eigvec_freq_', 'w')
f.write("%s  %s  %s\t %s\t %s\t %s \t%s \t%s\t %s\n"%('atom_id', 'atom_type', 'x', 'y', 'z', 'e_x', 'e_y', 'e_z', 'freq(cm-1)'))
counter = 0
freqs = []
eig_vec_mw = []
for i in range(natom*3):
  if frequencies[0][0][i] < max_freq:   # cut within 30THz
    freqs.append(frequencies[0][0][i]*33.35641)     # in cm-1
    eig_vec_mw.append(eigvecs[0][0][:, i])
    counter = counter + 1
index = counter 
print(f"Number of modes within {max_freq} THz:{index}")


# eigvectors within cutoff
for i in range(index):
  eig_vec_mw[i] = eig_vec_mw[i].reshape(natom, 3)

## eigvectors normalization 
#for i in range(index):
#  for j in range(natom):
#    if mol_id[j] == 1:
#      eig_vec_mw[i][j] = (1/(np.sqrt(95.94)))*eig_vec_mw[i][j]
#    elif mol_id[j] == 2 or mol_id[j] == 3:
#      eig_vec_mw[i][j] = (1/(np.sqrt(78.96)))*eig_vec_mw[i][j]
#    elif mol_id[j] == 4:
#      eig_vec_mw[i][j] = (1/(np.sqrt(183.84)))*eig_vec_mw[i][j]
#    elif mol_id[j] == 5 or mol_id[j] == 6:
#      eig_vec_mw[i][j] = (1/(np.sqrt(78.96)))*eig_vec_mw[i][j]

for i in range(index):
  eig_vec_mw[i] = eig_vec_mw[i]/np.linalg.norm(eig_vec_mw[i])
  print("Norm", np.sqrt(np.sum(eig_vec_mw[i]**2)))
  print("Shape", eig_vec_mw[i].shape)
  for j in range(natom):
    # write in text format
    f.write("%d %d %f %f %f %0.5f %0.5f %0.5f %0.5f %0.5f %0.5f  %f\n"%(at_id[j], mol_id[j], x[j], y[j], z[j], eig_vec_mw[i][j][0].real, eig_vec_mw[i][j][0].imag, eig_vec_mw[i][j][1].real, eig_vec_mw[i][j][1].imag, eig_vec_mw[i][j][2].real, eig_vec_mw[i][j][2].imag, freqs[i]))
f.close() 

end = time.time()
print("Total time taken :", end-start)
