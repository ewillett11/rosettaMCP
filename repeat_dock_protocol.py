from pyrosetta import *
from pyrosetta.rosetta import *
import sys
import os
import argparse
#import numpy as np
#import random

##remove contents of Score.txt
with open('Score.txt','a') as score_file:
    score_file.truncate(0)

nstruct = 10
binder_folder = 'binder_test'
complex_name = 'complex_0001_1.pdb'
sequence_14_xtal = 'FDATRERQIIPFLC'
sequence_14_binder = 'FSRDSYYD-S-R-C'

one_letter_AA = ['A','R','N','D','C','E','Q','G','H','I',
                 'L','K','M','F','P','S','T','W','Y','V']
three_letter_AA = ['ALA','ARG','ASN','ASP','CYS','GLU','GLN','GLY','HIS','ILE',
                   'LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL']

##pull out differences in sequence
count_AA = 0
AA_mut = []
NCAA_list = []
pos_mut = []
for x in range(0,len(sequence_14_binder)):
    if sequence_14_binder[x] != sequence_14_xtal[x]:
        count_AA = 1
        if sequence_14_binder[x] == '-':
            NCAA = input('Enter 3 letter NCAA: ')
            NCAA_space = ''.join([NCAA,' '])
            AA_mut.append(NCAA_space)
            NCAA_list.append(NCAA_space)
            pos_space = ''.join([str(x+1),' '])
            pos_mut.append(pos_space)
        else:
            index = one_letter_AA .index(sequence_14_binder[x])
            AA_3letter = three_letter_AA[index]
            AA_3letter_space = ''.join([AA_3letter,' '])
            AA_mut.append(AA_3letter_space)
            pos_space = ''.join([str(x+1),' '])
            pos_mut.append(pos_space)

##Combine mutations into one flag
if count_AA == 1:
    AA_mut_combine =''.join(AA_mut)
    pos_mut_combine = ''.join(pos_mut)
    NCAA_combine = ''.join(NCAA_list)
    flag_all = [' --aa_name "',AA_mut_combine[0:len(AA_mut_combine)-1],'" --position "',pos_mut_combine[0:len(pos_mut_combine)-1],'"',' --NCAAs "',NCAA_combine[0:len(NCAA_combine)-1],'" --pdb_name ',binder_folder]
##if the sequence is exactly the same, run flag where no AA is changed
elif count_AA == 0:
    NCAA_combine = 'BIP'
    flag_all = [' --aa_name ','PHE',' --position ','12',' --NCAAs ',NCAA_combine,' --pdb_name ',binder_folder]

#Combine flag_all into one string
flag_all_str = ''.join(flag_all)
print(flag_all_str)

##enter correct folder
cd_folder = ''.join(['cd /Users/willete3/Macrocycles/macrocycles_AW/Kd_data/hNSP4_MC_Jocelyn/AW_pyros/',binder_folder])
print(cd_folder)
os.system(cd_folder)

###run AW_Pyrosetta_dock.py nstruct times
for x in range(0,nstruct):
    run_AW_dock = ''.join(['/usr/local/bin/python3 AW_Pyrosetta_dock.py ',complex_name,flag_all_str,'_',str(x+1)])
    print(run_AW_dock)
    os.system(run_AW_dock)