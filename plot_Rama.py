import sys
import os
import re
import matplotlib.pyplot as plt

count = 0

with open('PhiPsi_mult.txt',"r") as file:
    readoutput = file.readlines()
    PHIphrase = 'phi'
    PSIphrase = 'psi'
    count = 0
    phi = []
    psi = []
    for line in readoutput:
        if PHIphrase in line:
            print(line[12:200])
            phi_d = float(line[12:200])
            #phi_degrees = (phi_a*180)/3.141592653
            phi.append(phi_d)
        if PSIphrase in line:
            print(line[12:200])
            print(float(line[12:200]))
            psi_d = float(line[12:200])
            #psi_degrees = (psi_a * 180) / 3.141592653
            psi.append(psi_d)

lengthphi = len(phi)
phi_adj = []
psi_adj = []
for x in range(0,lengthphi):
    if phi[x] != 0 and psi[x] != 0:
        phi_adj.append(phi[x])
        psi_adj.append(psi[x])
print(phi_adj)
print(psi_adj)
x_xaxis = [0,0,0,0,0]
y_xaxis = [-200,-100,0,100,200]
x_yaxis = [-200,-100,0,100,200]
y_yaxis = [0,0,0,0,0]

plt.xlim(-180, 180)
plt.ylim(-180, 180)

plt.scatter(phi_adj,psi_adj,color='black')
plt.plot(x_xaxis, y_xaxis,color = 'grey', linestyle = 'solid')
plt.plot(x_yaxis, y_yaxis,color = 'grey', linestyle = 'solid')

plt.ylabel('phi')
plt.xlabel('psi')
plt.title('RAMA')
plt.show()