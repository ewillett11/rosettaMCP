import sys
import os
import re
import matplotlib.pyplot as plt

count = 0

with open('out_simple_silent',"r") as file:
    readoutput = file.readlines()
    RMSDphrase = 'SCORE:  '
    score = []
    count = 0
    state = []
    score_str = []
    RMSD = []
    RMSD_str = []
    for line in readoutput:
        if RMSDphrase in line:
            count = count + 1
            if count == 1:
                print('SKIP')
            else:
                SCOREnum_str = line[8:20]
                RMSDnum_str = str(line[278:289])
                SCOREnum = float(line[8:20])
                RMSD_num = float(line[278:289])
                if SCOREnum >= 80:
                    print('Score >= 80')
                else:
                    score.append(SCOREnum)
                    score_str.append(SCOREnum_str)
                    state.append(count-1)
                    RMSD.append(RMSD_num)
                    RMSD_str.append(RMSDnum_str)

lengthRMSD = len(score)
lengthscore = len(RMSD)
print(lengthRMSD)
print(lengthscore)

plt.scatter(RMSD,score,color='blue')
plt.ylabel('Score')
plt.xlabel('RMSD')
plt.title('Rosetta (SimpleCycPepPredict)')
plt.show()