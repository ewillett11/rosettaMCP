######import dependencies
import pyrosetta
pyrosetta.init()

######send pdb files as a pose
p = pyrosetta.io.pose_from_pdb("6be7.pdb")

##remove contents
with open('PhiPsi_mult.txt','a+') as pp_File:
    pp_File.truncate(0)

######psi and phi and write into PhiPsi_mult
for i in range(1, p.total_residue() + 1):
    print(i,"phi =",p.phi(i),"psi =", p.psi(i))
    with open('PhiPsi_mult.txt','a+') as pp_File:
        phi_line = ''.join([str(i),"   phi =   ",str(p.phi(i)),'\n'])
        pp_File.write(phi_line)
        psi_line = ''.join([str(i),"   psi =   ",str(p.psi(i)),'\n'])
        pp_File.write(psi_line)