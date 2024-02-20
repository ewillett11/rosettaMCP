######import dependencies
import pyrosetta
pyrosetta.init()

######send pdb files as a pose
p = pyrosetta.io.pose_from_pdb("6be7.pdb")

######psi and phi
for i in range(1, p.total_residue() + 1):
    print(i,"phi =",p.phi(i),"psi =", p.psi(i))
