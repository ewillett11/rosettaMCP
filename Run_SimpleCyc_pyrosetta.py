from pyrosetta import *
from pyrosetta.rosetta import *
import sys
import os
import argparse

##Check to see what files are in the folder
#(this is to see if native file is in there)
all_files = os.system('ls > output.txt')
all_pdb = []
with open('output.txt', 'r') as flag_file:
    phrase_pdb = '.pdb'
    for line in flag_file:
        if phrase_pdb in line:
            all_pdb.append(line)
all_pdb_str = ''.join(all_pdb)
print(all_pdb_str)

###Enter sequence (right now only capability for CAAs)
print('Input the AA sequence (i.e. FGTIYLPC or DDPTPRQQ) '
      '\nIf there is an NCAA, enter "-" (i.e. enter FGT[NLU]YLPC as FGT-YLPC)'
      '\nnote: Cterm and Nterm modifications or Lariat bonds will be prompted later')
sequence_1L = input('ENTER SEQUENCE: ')
print('\n')

one_letter_AA = ['A','R','N','D','C','E','Q','G','H','I',
                 'L','K','M','F','P','S','T','W','Y','V']
three_letter_AA = ['ALA','ARG','ASN','ASP','CYS','GLU','GLN','GLY','HIS','ILE',
                   'LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL']

##pull out differences in sequence
count_NCAA = 0
AA_3_sequence = []
NCAA_list = []
for x in range(0,len(sequence_1L)):
    if sequence_1L[x] == '-':
        count_NCAA = 1
        NCAA = input('Enter 3 letter NCAA (in order from N to C terminus): ')
        AA_3_sequence.append(NCAA)
        NCAA_list.append(NCAA)
    else:
        index = one_letter_AA.index(sequence_1L[x])
        AA_3letter = three_letter_AA[index]
        AA_3_sequence.append(AA_3letter)

##Enter number of iterations
nstruct = input('\nNumber of Iterations (ex 500): ')
while nstruct.isnumeric() is False:
    print('\nPlease enter a number')
    nstruct = input('Number of Iterations (ex 500): ')


##Prompt for a native file
native = input('\nAdd a native file? [y/n]: ')
while native != 'y' and native != 'n':
    print('\nPlease enter either y or n')
    native = input('Add a native file? [y/n]: ')
if native == 'y':
    print('\nEnter native file (i.e. native.pdb) ')
    native_file = input('Native file name: ')
    ##check if native pdb is in folder
    quit_num = -1
    while quit_num != 0:
        if native_file in all_pdb_str:
            native_line = ''.join(['\n-in:file:native ', native_file])
            print('Native file is in folder. Begin Simulation')
            quit_num = 0
            break
if native == 'n':
    native = '6be7.pdb'

##Combine mutations into one flag
sequence_combine =''.join(sequence_1L)
if count_NCAA == 1:
    NCAA_combine = ' '.join(NCAA_list)
    flag_all = ['seq.txt',' --nstruct ',nstruct,' --NCAAs "',NCAA_combine,'" --pdb_name ','test']
##if the sequence is exactly the same, run flag where no AA is changed
elif count_NCAA == 0:
    NCAA_combine = 'BIP'
    flag_all = ['seq.txt',' --nstruct ',nstruct,' --NCAAs "',NCAA_combine,'" --pdb_name ','test']

#Combine flag_all into one string
flag_all_str = ''.join(flag_all)
print(flag_all_str)

###run AW_Pyrosetta_dock.py nstruct times
run_SCPP = ''.join(['/usr/local/bin/python3 SimpleCycPepPredict_pyrosetta.py ',native_file,' ',flag_all_str,'_',str(x+1)])
print(run_SCPP)
os.system(run_SCPP)