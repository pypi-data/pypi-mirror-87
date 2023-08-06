import numpy as np
from matplotlib import pyplot as plt

def findPeriod(list, period):
    '''For a list of times (relative to a sync pulse) calculate the average time deviation squared.  
    '''
    residuum = []
    sum_residuum = 0
    for each in list:
        r = each % period
        residuum.append(r)
        sum_residuum += r
    av_res = sum_residuum / len(list)
    deviation = 0
    for res in residuum:
        deviation += (res - av_res)**2
    deviation /= (len(residuum)*period**2)
    return deviation, av_res

def makeTimeRelative(times, durations):
    list = []
    synced = False
    t_zero = 0
    for each in pulses:
        if synced:
            list.append(pulses[each][0]-t_zero)
        if 9000 < pulses[each][2] < 9800:
            print("synced")
            t_zero = pulses[each][0]
            synced = True
    return list

data = []       # read dat from file [[time in microsec, low duration, high duration], [...], ...]
with open("data433_Signal2.txt", 'r') as f:
    for line in f:
        data.append([int(each) for each in line.split(',')])

sumOn = 0; sumOff = 0
for pulse in data[1:]:
    sumOn += pulse[2]
    sumOff += pulse[1]
sumOn /= len(data)
sumOff /= len(data)

print("Average on and off times:", sumOn, sumOff)
