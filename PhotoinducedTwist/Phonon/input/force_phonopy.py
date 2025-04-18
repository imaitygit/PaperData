# Force constants script 

# Import stuffs  
from phonolammps import Phonolammps
from phonopy import Phonopy
import pickle
from phonopy.structure.atoms import PhonopyAtoms
import numpy as np
from atom_position import *
import time 
import gzip


#Input part 
natom, a_1, a_2, a_3 = get_lattice('lammps.dat') 
at_id, mol_id, x, y, z = get_position('lammps.dat', natom)
print ("natom :", natom, flush=True)

# cells, supercell [covergeed!!!]
phlammps = Phonolammps('in.phonon',
                       supercell_matrix=[[6, 0, 0],
                                         [0, 6, 0],
                                         [0, 0, 1]])
unitcell = phlammps.get_unitcell()

# get the force constants
st_1 = time.time()
force_constants = phlammps.get_force_constants()

# save fcs
if force_constants is not None:
    pickle.dump(force_constants, gzip.open("FORCE_CONSTANTS", "wb"), protocol=4)

en_1 = time.time()
print("Time (force cnstant calculations :)", en_1-st_1 )
