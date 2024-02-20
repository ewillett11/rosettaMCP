from pyrosetta import *
from pyrosetta.rosetta import *
import sys
import os
import argparse
#import numpy as np
#import random

init('-score:weights ref2015_cart')

parser = argparse.ArgumentParser()
parser.add_argument('filename', default='complex_0001_1.pdb')
parser.add_argument('--position', required=True, type = list)
parser.add_argument('--aa_name', required=True, type = list)
parser.add_argument('--pdb_name', default='test.pdb')
parser.add_argument('--NCAAs', required=False, type = list)

args = parser.parse_args()
#Enter nstruct of docking
nstruct = 5

##split up AA and position and NCAAs:
count_AA = 0
AA_list = []
aa_name1 = args.aa_name
for a in range(0,len(aa_name1)):
    if aa_name1[a] == ' ':
        AA = ''.join(aa_name1[count_AA:a])
        AA_list.append(AA)
        count_AA = a+1
    elif a == len(aa_name1)-1:
        AA = ''.join(aa_name1[count_AA:len(aa_name1)])
        AA_list.append(AA)
print(AA_list)

count_pos = 0
pos_list = []
position1 = args.position
for a in range(0,len(position1)):
    if position1[a] == ' ':
        pos = ''.join(position1[count_pos:a])
        pos_list.append(int(pos))
        count_pos = a+1
    elif a == len(position1)-1:
        pos = ''.join(position1[count_pos:len(position1)])
        pos_list.append(int(pos))
print(pos_list)

count_NCAA = 0
NCAA_list = []
ncaa_name1 = args.NCAAs
for a in range(0,len(ncaa_name1)):
    if ncaa_name1[a] == ' ':
        NCAA = ''.join(ncaa_name1[count_NCAA:a])
        NCAA_list.append(NCAA)
        count_NCAA = a+1
    elif a == len(ncaa_name1)-1:
        NCAA = ''.join(ncaa_name1[count_NCAA:len(ncaa_name1)])
        NCAA_list.append(NCAA)
print(NCAA_list)


# read in complex PDB
pose = pose_from_file(args.filename)
sfxn = core.scoring.get_score_function()

##param files name
print(len(NCAA_list))
params_filenames = pyrosetta.rosetta.utility.vector1_string(len(NCAA_list))
for x in range(0,len(NCAA_list)):
    param_name = ''.join([NCAA_list[x],'.params'])
    print(param_name)
    params_filenames[x+1] = param_name
rts = pyrosetta.generate_nonstandard_residue_set(pose, params_filenames)

# Set up variant types -- the correct acetylation type and the cysteine-with-bond
# type necessary for the thioether chemistry. (Long story short, but it's impossible
# for PDB I/O to automatically 'know' that the LACK of atoms (like HG on a Cys) means
# that there should be a variant type.)
mvtm = protocols.simple_moves.ModifyVariantTypeMover()
mvtm.set_additional_type_to_add(
    'ACETYLATED_NTERMINUS_CONNECTION_VARIANT'
)
mvtm.set_additional_type_to_remove(
    'ACETYLATED_NTERMINUS_VARIANT'
)
mvtm.set_residue_selector(core.select.residue_selector.ResidueIndexSelector('1C'))
mvtm.apply(pose)

mvtm = protocols.simple_moves.ModifyVariantTypeMover()
mvtm.set_additional_type_to_add(
    'SC_BRANCH_POINT'
)
mvtm.set_residue_selector(core.select.residue_selector.ResidueIndexSelector('14C'))
mvtm.apply(pose)



# Declare a bond between the thioether linkage atoms. This might not be necessary.
# We hope cart_bonded helps preserve the geometry.
db = protocols.simple_moves.DeclareBond()
db.set(
    res1=pose.pdb_info().pdb2pose('C', 1),
    atom1='CP2',
    res2=pose.pdb_info().pdb2pose('C', 14),
    atom2='SG',
    add_termini=False
)
db.apply(pose)


# write out starting macrocycle sequence, so that you're confident we've got it right
# this will print initial NCAAs as X; that's OK.
#
# note that this assumes the complex PDB lists the macrocycle as the second chain, a
# pretty common convention. in theory you could use a variety of methods to figure out
# "the chain you mean" for these purposes. (really all we care about is giving you a
# nice way to index the residue you want to mutate!)
print(pose.chain_sequence(2))



# Long term, we probably will want to add a command line arg for the chain letter.
pose_idx = []
for x in range(0,len(pos_list)):
    print(pos_list[x])
    pose_i = pose.pdb_info().pdb2pose('C', pos_list[x])
    pose_idx.append(pose_i)
print(pose_idx)



# mutate the residue of interest
for x in range(0,len(AA_list)):
    mut = protocols.simple_moves.MutateResidue(pose_idx[x], AA_list[x])
    # I'm not sure if this is a good idea, but it's not unreasonable
    mut.set_preserve_atom_coords(True)
    mut.apply(pose)



# relax just a sphere around the mutated residue.
mutate_l = []
for x in range(0,len(pos_list)):
    mutate_l.append(str(pos_list[x]))
    mutate_l.append('C,')
mutate_list = ''.join(mutate_l)
mutate_list_short = mutate_list[0:len(mutate_list)-1]
print(mutate_list_short)
mutated = core.select.residue_selector.ResidueIndexSelector(mutate_list_short)
neighbs = core.select.residue_selector.NeighborhoodResidueSelector(mutated, 8.0, True)
not_neighbs = core.select.residue_selector.NotResidueSelector(neighbs)

oors = core.pack.task.operation.OperateOnResidueSubset(core.pack.task.operation.PreventRepackingRLT(), not_neighbs)
rtrp = core.pack.task.operation.OperateOnResidueSubset(core.pack.task.operation.RestrictToRepackingRLT(), neighbs)

tf = core.pack.task.TaskFactory()
tf.push_back(core.pack.task.operation.IncludeCurrent())
tf.push_back(oors)
tf.push_back(rtrp)

frlx = protocols.relax.FastRelax(sfxn, 5)

# only minimize residues 
mm = core.kinematics.MoveMap()
n = neighbs.apply(pose)
for ii, bb in enumerate(n):
    mm.set_bb(ii+1, bb)
    mm.set_chi(ii+1, bb)    
frlx.set_movemap(mm)
frlx.cartesian(True)

frlx.set_task_factory(tf)
frlx.apply(pose)

##pull out sequence
seq = pose.sequence()
for x in range(0,len(seq)):
    if seq[x] == 'Z':
        seq_MC = seq[x+4:len(seq)]
        break
print('seq MC: ',seq_MC)
with open('Score.txt','a') as score_file:
    line_seq = ''.join(['\nsequence MC: ',seq_MC,'\n'])
    score_file.write(line_seq)

##get interface score
ia = protocols.analysis.InterfaceAnalyzerMover(
    dock_chains='A_C',
    tracer=False,
    sf=sfxn,
    compute_packstat=False,
    pack_input=False,
    pack_separated=False,
    use_jobname=False,
    detect_disulfide_in_separated_pose=False
)
ia.set_scorefunction(sfxn)
ia.apply(pose)
print(ia.show())

with open('Score.txt','a') as score_file:
    line_complex = ''.join(['complex_energy: ', str(ia.get_complex_energy()),'\n'])
    print('complex_energy: ', ia.get_complex_energy())
    score_file.write(line_complex)
    line_sepdG = ''.join(['sep_interface_dG: ', str(ia.get_separated_interface_energy()),'\n'])
    print('sep_interface_dG: ', ia.get_separated_interface_energy())
    score_file.write(line_sepdG)
    line_intdG = ''.join(['interface_dG: ', str(ia.get_interface_dG()),'\n'])
    print('interface_dG: ', str(ia.get_interface_dG()))
    score_file.write(line_intdG)
    #print('separated_interface_energy_ratio: ', ia.get_separated_interface_energy_ratio())
    line_int_dhb = ''.join(['interface_delta_hbond_unsat: ', str(ia.get_interface_delta_hbond_unsat()),'\n'])
    print('interface_delta_hbond_unsat: ', ia.get_interface_delta_hbond_unsat())
    score_file.write(line_int_dhb)
    line_d_sasa = ''.join(['interface_delta_sasa: ', str(ia.get_interface_delta_sasa()),'\n'])
    print('interface_delta_sasa: ', ia.get_interface_delta_sasa())
    score_file.write(line_d_sasa)

##print scores
totalscore = sfxn(pose)
print('score after relax: ',totalscore)
print(sfxn.show(pose))
pdbname = ''.join([args.pdb_name,'.pdb'])
pose.dump_pdb(pdbname)
#while not jd.job_complete:     
    #jd.output_decoy(pose) 
#pose.dump_score_pdb('test.pdb', sfxn)

quit()