#!/bin/bash

#Using the TWISTER package, we generate data for the
#MoSe2/WSe2 heterostructure.

#------------------------------------------------
# Path to hex.table, twister.py, auxillary files and basis position
base_path="/Users/indrajitmaity/Codes/GitHub"
hextable="${base_path}/PaperData/PhotoinducedTwist/Structure"
twister_path="${base_path}/Twister/SRC"
aux_files="$hextable/aux_files"
basis_file="$aux_files/basis_60"

# Skip first few lines when reading hex table
skiplines=3 
# lattice constant (in angstrom)
latcon=3.32
# Initial guess for the separation between the two layers
# (Mo–W). The force field will adjust it during relaxation.
dz=5.9
# Index of twist angle to start from (must be an integer)
init=10
# Index up to which structures will be created (must be an integer)
end=10
# Step size between indices (must be an integer ≥1)
step=1

# Do not directly perform relaxation, as LAMMPS may not be 
# installed.
lammps_relax=false
forcefield=""
style="use_python"
lammps_path="/home/user/codes/python_wrapper/lammps-30Mar18/src"
#-------------------------------------------------
#-------------------------------------------------



# Generate hex.table if not found 
if [ ! -f $hextable/hex.table ]; then
  echo "hex.table is not found! Generating one for twisted homo-bilayer systems"
  echo "Please ensure this is what you want"
  printf "$latcon" | python3 $aux_files/hex_table_least.py 
  # If you want to generate more general cases 
  # instead of hex_table_least.py use the following line
  #printf "$latcon" | python $aux_files/hex_table_generic.py
  cp -n hex.table $hextable
fi

# automated structure generation
for ((i=init; i<=end; i=i+step));  # c-style loop
do	
  Counter=0
  while read line
  do
   # skip first few lines of hex.table
    if [ $Counter -ge $skiplines ]; then
      index=$(echo $line | awk '{print $1}')
      if [ $i -eq $index ]; then 
        theta=$(echo $line | awk '{print $2}')
        echo "twist_angle (in degree) $theta"
        mkdir twist_$theta; cd twist_$theta
        m=$(echo $line | awk '{print $3}')
        n=$(echo $line | awk '{print $4}')
        p=$(echo $line | awk '{print $5}')
        q=$(echo $line | awk '{print $6}')
        theta_rad=$(echo $line | awk '{print $7}')
#        paste <(echo "$index") <(echo "$i")
        # Create input file for Twister
        cat > twist.inp << EOF 
a1_l:
0.5 0.8660254 0.0
a2_l:
-0.5 0.8660254 0.0
a3_l:
0.0 0.0 1.0

celldm1_l, celldm2_l, celldm3_l: (Angstrom)
$latcon $latcon 35.000000

a1_u:
0.5 0.8660254 0.0
a2_u:
-0.5 0.8660254 0.0
a3_u:
0.0 0.0 1.0

celldm1_u, celldm2_u, celldm3_u: (Angstrom)
$latcon $latcon 35.000000

angle: (radians)
$theta_rad

layer2_from_file:
True basis_pos_crys_l2

translate_z: (Angstrom)
$dz

Superlattice1: (m,n)
$m $n


Superlattice2: (p,q)
$p $q

Plot_lattice:
False

EOF
        # creation of rigidly twisted structure
        cp $basis_file/basis_pos_crys* .
        python3 $twister_path/twister.py twist.inp

        # creation of quantum espresso input file
        # [] reads a0 as lattice constant
        cp $aux_files/toqe.py ./
        python3 toqe.py
        rm toqe.py

        # creation of lammps data file       
        cp $aux_files/lammps_triclinic.py ./
        cp $aux_files/Mass_FF ./
        python3 lammps_triclinic.py
        rm lammps_triclinic.py

        # prepare lammps input file
        cp $aux_files/tolammps.py ./
        python3 tolammps.py
        rm tolammps.py

        # lammps minimization (serial) 
        if [ "$lammps_relax" = true ]; then
          echo "will perform relaxation"
          cp $forcefield/* .
          if [[ $style = use_python ]]; then
            echo "will be using python wrapper for lammps" 
            cp $aux_files/run_lammps.py ./
            cp $aux_files/extract_pos.py ./
            python3 run_lammps.py
            python3 extract_pos.py
          else
            echo "will be using standard lammps executable"
            cp $aux_files/extract_pos.py ./
            $lammps_path/lmp_serial -in lammps.in
            python3 extract_pos.py
          fi
        fi
        cd ../
      fi
    fi
    Counter=`expr $Counter + 1`
  done < $hextable/hex.table
done			
echo "============================="
echo "Done!"
echo "============================="
