import sys
import os

##remove contents of sequence file
with open('seq.txt','w') as seq_file:
    seq_file.truncate(0)

##remove nstruct and native file from flag file
with open("simple.flags", "r") as f:
    lines = f.readlines()
with open("simple.flags", "w+") as f:
    for line in lines:
        if "nstruct" in line:
            print('remove ',line)
        elif "in:file:native" in line:
            print('remove ',line)
        elif "cyclization_type" in line:
            print('remove ',line)
        else:
            f.write(line)

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

##pull out differences in sequence
count_AA = 0
AA_3_sequence = []
NCAA_list = []
for x in range(0,len(sequence_1L)):
    if sequence_1L[x] == '-':
        NCAA = input('Enter 3 letter NCAA (in order from N to C terminus): ')
        AA_3_sequence.append(NCAA)
        NCAA_list.append(NCAA)
    else:
        index = one_letter_AA.index(sequence_1L[x])
        AA_3letter = three_letter_AA[index]
        AA_3_sequence.append(AA_3letter)

print('AA 3 letter sequence: ',AA_3_sequence)

##Prompt if there are any tail residues (is it a lariat)
Tail = input('\nDoes it NOT have an n_to_c_amide_bond (ie LARIAT, THIOETHER,TERMINAL DISULFIDE etc? [y/n]: ')
while Tail != 'y' and Tail != 'n':
    print('\nPlease enter either y or n')
    Tail = input('\nDoes it NOT have an n_to_c_amide_bond (ie LARIAT, THIOETHER,TERMINAL DISULFIDE etc? [y/n]: ')
with open('simple.flags','a+') as flag_file:
    if Tail == 'y':
        print('Enter which residues connect in the lariat\n'
              '(i.e. if residue 1 connects with residue 9 enter 1, then enter 9):')
        first_lariat_res = int(input('Enter first residue connect: '))
        if first_lariat_res >= len(sequence_1L)-1:
            print('Code is quitting because lariat residues are impossible')
            quit()
        end_lariat_res = int(input('Enter end residue connect: '))
        if end_lariat_res >= len(sequence_1L)+1:
            print('Code is quitting because lariat residues are impossible')
            quit()
        ###prompt user to find closure bond
        print('\n0) For n_to_c_amide_bond enter 0\n'
              '1) terminal_disulfide 1\n'
              '2) thioether_lariat enter 2\n'
              '3) nterm_isopeptide_lariat 3\n'
              '4) cterm_isopeptide_lariat 4\n'
              '5) sidechain_isopeptide 5')
        Tail_num = int(input('Enter 0,1,2,3,4: '))
        if Tail_num == 1:
            flag_file.write('\n-cyclic_peptide:cyclization_type terminal_disulfide')
        elif Tail_num == 2:
            flag_file.write('\n-cyclic_peptide:cyclization_type thioether_lariat')
        elif Tail_num == 3:
            flag_file.write('\n-cyclic_peptide:cyclization_type nterm_isopeptide_lariat')
            index_lariat = ''.join(['\n-cyclic_peptide:lariat_sidechain_index ',str(end_lariat_res)])
            flag_file.write(index_lariat)
        elif Tail_num == 4:
            flag_file.write('\n-cyclic_peptide:cyclization_type cterm_isopeptide_lariat')
            index_lariat = ''.join(['\n-cyclic_peptide:lariat_sidechain_index ', str(first_lariat_res)])
            flag_file.write(index_lariat)
        elif Tail_num == 5:
            flag_file.write('\n-cyclic_peptide:cyclization_type sidechain_isopeptide')
            index_lariat = ''.join(['\n-cyclic_peptide:sidechain_isopeptide_indices ',str(first_lariat_res),' ',str(end_lariat_res)])
            flag_file.write(index_lariat)
        else:
            flag_file.write('\n-cyclic_peptide:cyclization_type n_to_c_amide_bond')
    else:
        flag_file.write('\n-cyclic_peptide:cyclization_type n_to_c_amide_bond')

##Prompt if there are any Nterm or Cterm modifications
NCterm = input('\nAre there any Nterm or Cterm modifications? [y/n]: ')
while NCterm != 'y' and NCterm != 'n':
    print('\nPlease enter either y or n')
    NCterm = input('Are there any Nterm or Cterm modifications? [y/n]: ')
if NCterm == 'y':
    NCterm_num = -1
else:
    NCterm_num = 0
while NCterm_num != 0:
    print('\n0) For no more modifications enter 0\n'
          '1) Nterm Acetylation enter 1\n'
          '2) Cterm amidation enter 2\n'
          '3) Cterm Methylation enter 3')
    NCterm_num = int(input('Enter 0,1,2,3: '))
    if NCterm_num == 1:
        Nterm1 = AA_3_sequence[0]
        AA_3_sequence[0] = ''.join([Nterm1,':AcetylatedNtermConnectionProteinFull'])
        print('Fixed AA 3 letter sequence: ',AA_3_sequence)
    if NCterm_num == 2:
        Nterm1 = AA_3_sequence[len(AA_3_sequence)-1]
        AA_3_sequence[len(AA_3_sequence)-1] = ''.join([Nterm1,':Cterm_amidation'])
        print('Fixed AA 3 letter sequence: ',AA_3_sequence)
    if NCterm_num == 3:
        Nterm1 = AA_3_sequence[len(AA_3_sequence)-1]
        AA_3_sequence[len(AA_3_sequence)-1] = ''.join([Nterm1,':MethylatedCtermProteinFull'])
        print('Fixed AA 3 letter sequence: ',AA_3_sequence)

##Add sequence to seq.txt file
with open('seq.txt','w') as seq_file:
    AA_3_combine = ' '.join(AA_3_sequence)
    print('\nAdding sequence to seq.txt: ', AA_3_combine)
    seq_file.write(AA_3_combine)

##Add nstruct and native pdb to flag file
with open('simple.flags','a+') as flag_file:
    ##Ask number of iterations
    nstruct = input('\nNumber of Iterations (ex 500): ')
    while nstruct.isnumeric() is False:
        print('\nPlease enter a number')
        nstruct = input('Number of Iterations (ex 500): ')
    else:
        nstruct_line = ''.join(['\n-nstruct ',nstruct])
        flag_file.write(nstruct_line)
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
                flag_file.write(native_line)
                print('Native file is in folder. Begin Simulation')
                quit_num = 0
                break
            else:
                print('Native file is not in folder')
                quit_num = int(input('\nTo quit enter 0, to try native file again enter 1: '))
                if quit_num == 0:
                    quit()
                else:
                    native_file = input('Native file name: ')

##Run SimpleCycPepPredict
SimpCyc = '~/rosetta.binary.mac.release-351/main/source/bin/simple_cycpep_predict.static.macosclangrelease @simple.flags'
print(SimpCyc)
os.system(SimpCyc)