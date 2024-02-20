from pyrosetta import *
from pyrosetta.rosetta import *
import sys
import os
import argparse

init('-score:weights ref2015_cart')

parser = argparse.ArgumentParser()
parser.add_argument('nativefile', default='6be7_s1.pdb')
parser.add_argument('--sequence', default='seq.txt')
parser.add_argument('--nstruct', required=True, type = list)
parser.add_argument('--pdb_name', default='test.pdb')
parser.add_argument('--NCAAs', required=False, type = list)

args = parser.parse_args()

#native = pose_from_file(args.nativefile)
#sfxn = core.scoring.get_score_function()

SCPP = pyrosetta.rosetta.protocols.cyclic_peptide_predict.SimpleCycpepPredictApplication(allow_file_read=True)
SCPP.set_sequence(args.sequence)
#SCPP.set_scorefxn(sfxn)
SCPP.set_native(args.nativefile)
SCPP.set_nstruct(args.nstruct)
SCPP.run()