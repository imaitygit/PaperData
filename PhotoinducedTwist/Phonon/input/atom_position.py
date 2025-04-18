import numpy as np 

def get_position(pos_file, natom):
  f = open(pos_file, 'r')
  lines = f.readlines()
  f.close()
  for i in range(len(lines)):
    if "Atoms # atomic" in lines[i]:
      at_id = [eval(lines[j].split()[0])\
              for j in range(i+2, i+natom+2)]
      mol_id = [eval(lines[j].split()[1])\
               for j in range(i+2, i+natom+2)]
      x = [eval(lines[j].split()[2])\
          for j in range(i+2, i+natom+2)]
      y = [eval(lines[j].split()[3])\
          for j in range(i+2, i+natom+2)]
      z = [eval(lines[j].split()[4])\
          for j in range(i+2, i+natom+2)]
      return at_id, mol_id, x, y, z
    if "Atoms # full" in lines[i]:
      at_id = [eval(lines[j].split()[0])\
              for j in range(i+2, i+natom+2)]
      mol_id = [eval(lines[j].split()[2])\
               for j in range(i+2, i+natom+2)]
      x = [eval(lines[j].split()[4])\
          for j in range(i+2, i+natom+2)]
      y = [eval(lines[j].split()[5])\
          for j in range(i+2, i+natom+2)]
      z = [eval(lines[j].split()[6])\
          for j in range(i+2, i+natom+2)]
      return at_id, mol_id, x, y, z
    

def get_eigvec(eigvec_file, natom):
  at_id, at_type, x, y, z, ex, ex_im, ey, ey_im,  ez, ez_im,  freq = np.loadtxt(eigvec_file, unpack=True, skiprows=1)
  modes = int(len(at_id)/natom)
  return modes, at_id.reshape(modes, natom), at_type.reshape(modes, natom), x.reshape(modes, natom), y.reshape(modes, natom), z.reshape(modes, natom), ex.reshape(modes, natom), ey.reshape(modes, natom), ez.reshape(modes, natom), freq.reshape(modes, natom)


def get_lattice(input_file):
  f = open(input_file, 'r')
  lines = f.readlines()
  f.close()
  a_1 = []
  a_2 = []
  a_3 = []
  for i in range(len(lines)):
    if "atoms" in lines[i]:
      natom = eval(lines[i].split()[0])
    elif "xlo xhi" in lines[i]:
      a_1.append(eval(lines[i].split()[0]))
      a_1.append(eval(lines[i].split()[1]))
    elif "ylo yhi" in lines[i]:
      a_2.append(eval(lines[i].split()[0]))
      a_2.append(eval(lines[i].split()[1]))
    elif "zlo zhi" in lines[i]:
      a_3.append(eval(lines[i].split()[0]))
      a_3.append(eval(lines[i].split()[1]))
    elif "xy xz yz" in lines[i]:
      a_2.append(eval(lines[i].split()[0]))
  return natom, a_1, a_2, a_3	
