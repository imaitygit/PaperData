# generic script 
# Phonon band structure and density of states and frequencies and eigenvectors 

# Import stuffs  
from phonolammps import Phonolammps
from phonopy import Phonopy
import numpy as np
import pickle
from phonopy.structure.atoms import PhonopyAtoms
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


# cells, supercell [covergeed!!!]
phlammps = Phonolammps('in.phonon',
                       supercell_matrix=[[6, 0, 0],
                                         [0, 6, 0],
                                         [0, 0, 1]])
unitcell = phlammps.get_unitcell()
# get the force constants

# load fcs
force_constants = pickle.load(gzip.open("FORCE_CONSTANTS", "rb"))
print ("Loaded the force constat matrix")

supercell_matrix = phlammps.get_supercell_matrix()


# use the force constants for post processing 
phonon = Phonopy(unitcell,
                 supercell_matrix)
phonon.set_force_constants(force_constants)
pcell = phonon.get_primitive()

# Band structure plot 
bands = []
q_start  = np.array([0.0, 0.0, 0.0])
q_1    = np.array([0.5, 0.0, 0.0])

qp = 1

# single qpoint calc 
band = []
for i in range(qp):
    band.append(q_start + (q_1 - q_start) / 1 * i)
bands.append(band)

phonon.run_band_structure(bands, with_eigenvectors=True)

# Extract specific ouptut
band_data = phonon.get_band_structure_dict()
q_points = band_data["qpoints"]
distances = band_data["distances"]
frequencies = band_data["frequencies"]
eigvecs = band_data["eigenvectors"]
group_vels = band_data.get("group_velocities", None)


# Save every eigenval and eigenvec unchanged
pickle.dump(frequencies, gzip.open("freq_phonopy", "wb"), protocol=4)
pickle.dump(eigvecs, gzip.open("eigvecs_phonopy", "wb"), protocol=4)
