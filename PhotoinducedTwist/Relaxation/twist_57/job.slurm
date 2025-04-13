#!/bin/bash --login

#SBATCH --job-name=ws2wse2
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:20:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=e05-gc-lis
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --reservation=shortqos


# Ensure that the environment is set correctly for the job
module load epcc-job-env

# Load the xthi module to get access to the xthi program
#module load xthi

# srun launches the parallel program based on the SBATCH options
# The SBATCH options are provided above
# This is an "only MPI" job.
LAMMPS=/work/e05/e05/imaity/codes/lammps-7Jan2022/src
srun --distribution=block:block --hint=nomultithread --unbuffered $LAMMPS/lmp_archer2 -i lammps.in -l lammps.out

