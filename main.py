#!/usr/local/epics/modules/pythonIoc/pythonIoc
from softioc import softioc, builder
import numpy as np
from Voltage import VOLTAGE
from Current import CURRENT
import time
filename="relayMatrix.txt"
relayCorMatrix = np.loadtxt(filename, delimiter="\t")
pattern = np.zeros([3, 16], dtype = int)
offset = np.loadtxt("offsetMatrix.txt")
magnet_offset = np.loadtxt("magnetOffsetMatrix.txt")

ListOfVoltages = []
ListOfCurrents = []
for i in xrange(0,3): #board
    for j in xrange(0,16): #channel 
        ListOfVoltages.append(VOLTAGE(i, j+1))
        ListOfCurrents.append(CURRENT(i, j+1, pattern, relayCorMatrix, offset, magnet_offset))
#run the ioc
builder.LoadDatabase()
softioc.iocInit()
#start the ioc shell
time.sleep(5)
#pattern[[1, 2]] = pattern[[2, 1]]
print(pattern)
softioc.interactive_ioc(globals())

