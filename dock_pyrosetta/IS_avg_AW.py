import sys
import os
import statistics

##Pull out brackets
count = 0
IS_all = []
IS_all_str = []
Score = []
Score_str = []
dH_all = []
dH_all_str = []
dGSA_all = []
dGSA_all_str = []

with open('Score.txt', "r+") as file:
    readoutput = file.readlines()
    phrase_SCORE = 'complex_energy:'
    phrase_dG = 'sep_interface_dG:'
    phrase_delH = 'interface_delta_hbond_unsat:'
    phrase_dGSA = 'interface_delta_sasa:'
    for line in readoutput:
        if phrase_SCORE in line:
            count = count + 1
            sc = float(line[15:32])
            Score.append(sc)
            Score_str.append(str(sc))
        if phrase_dG in line:
            IS = float(line[17:32])
            IS_all.append(IS)
            IS_all_str.append(str(IS))
        if phrase_delH in line:
            dH = float(line[29:33])
            dH_all.append(dH)
            dH_all_str.append(str(dH))
        if phrase_dGSA in line:
            dSASA = float(line[22:40])
            dGSA = dSASA/IS
            dGSA_all.append(dGSA)
            dGSA_all_str.append(str(dGSA))

print('IS: ',IS_all)
print('Score: ',Score)
print('delta Hbond Unsat: ',dH_all)
print('interface_delta_sasa/dG: ',dGSA_all)

IS_total = 0
Score_total = 0
dH_total = 0
dGSA_total = 0
for x in range(0,len(IS_all)):
    IS_total = IS_total + IS_all[x]
    Score_total = Score_total + Score[x]
    dH_total = dH_total + dH_all[x]
    dGSA_total = dGSA_total + dGSA_all[x]

score_avg = Score_total/len(Score)
score_stdev = statistics.stdev(Score)
IS_avg = IS_total/len(IS_all)
IS_stdev = statistics.stdev(IS_all)
dH_avg = dH_total/len(dH_all)
dH_stdev = statistics.stdev(dH_all)
dGSA_avg = dGSA_total/len(dGSA_all)
dGSA_stdev = statistics.stdev(dGSA_all)

Kd_all = []
for a in range(0,len(IS_all)):
    logKd = (IS_all[a] + 3.54)/0.55
    Kd = 10**(logKd)
    Kd_all.append(Kd)

print('\n\n')
print('Score avg: ',score_avg)
print('Score STDEV: ',score_stdev)
print('Interface score avg: ',IS_avg)
print('Interface score STDEV: ',IS_stdev)
print('delta Hbond Unsat avg: ',dH_avg)
print('delta Hbond Unsat STDEV: ',dH_stdev)
print('Interface_delta_sasa/dG avg: ',dGSA_avg)
print('Interface_delta_sasa/dG STDEV: ',dGSA_stdev)
print('\n')
print('IS_all: ',IS_all)
print('Kd all: ',Kd_all)

##write in Score.txt
with open('Score.txt', "a+") as file:
    score_line = ''.join(['\nScore: ',str(round(score_avg,2)),u"\u00B1",str(round(score_stdev,2)),'\n'])
    file.write(score_line)
    IS_line = ''.join(['dG sep: ',str(round(IS_avg,2)),u"\u00B1",str(round(IS_stdev,2)),'\n'])
    file.write(IS_line)
    dH_line = ''.join(['Delta Unsat Hbond: ',str(round(dH_avg,2)),u"\u00B1",str(round(dH_stdev,2)),'\n'])
    file.write(dH_line)
    dGSA_line = ''.join(['dSASA/dG: ',str(round(dGSA_avg,2)),u"\u00B1",str(round(dGSA_stdev,2)),'\n'])
    file.write(dGSA_line)