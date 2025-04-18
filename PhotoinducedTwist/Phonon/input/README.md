# Example scripts to perform phonon calculations
------------------------------------------------

## Packages required
1. [LAMMPS](https://www.lammps.org/)
2. [Phonopy](https://phonopy.github.io/phonopy/)
3. [PhonoLAMMPS](https://github.com/abelcarreras/phonolammps)
4. Python packages, such as, Numpy etc. 



## How to
1. Run `python force_phonopy.py` to generate
`FORCE_CONSTANTS` 
2. Run `python bands_phonopy.py` to generate phonon
frequencies and eigenvectors at the $\Gamma$ point.
3. Run `python modes.py` to create `atom_eigvec_*` for post-processing.
4. The process is the same for both unit cells and twisted
bilayers, although calculations for twisted bilayers are
significantly more computationally expensive.

## Data 
Phonon mode data (`atom_eigvec_freq_*`) for 2.1° and
56.86° twisted MoSe₂/WSe₂ structures is included in this
directory.
