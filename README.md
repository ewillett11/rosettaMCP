Using Simple Cyc Pep predict

RUN SimpleCycPepPredict.py
Will prompt inputs and run SimpleCycPep.py predict in rosetta

--Enter sequence

--Enter number of iterations

--SOME capability of NCAAs

--Opporunity for Nterminus and Cterminus modifications

--Working to adapt tail residues/other cyclization closures

REQUIRES ROSETTA DOWNLOAD

RUN phipsi.py
--determine phi and psi angles of native structure and conformers
--results printed to PhiPsi_mult.txt
Run plot_Rama.py to visualize phi/psi plots

RUN RMSD_scoreplots_simple
--plots silent file RMSD vs score

NOTE:
Working on running in pyrosetta (in pyrosetta folder)

Docking (folder: dock_pyrosetta)

RUN repeat_dock_protocol.py
Will prompt inputs and run AW_Pyrosetta_dock.py with pyrosetta
--arguments: need complex pdb file, sequence of MCP
--Can be adabptable to NCAAs
--output sent to Score.txt

RUN IS_avg_AW.py (run after repeat_dock_protocol.py to average and analyze)
--output (average +/- standard deviation sent to Score.txt
-- Score, dG sep, Delta Unsat Hbond, dSASA/dG
