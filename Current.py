from softioc import builder, softioc
from epics import PV
import numpy as np

class CURRENT():
    def __init__(self, board_num, chan_num, pattern, relayCorrMatrix, offset, magnetOffset):
        self.pattern = pattern
        self.board_num = board_num
        self.chan_num = chan_num
        self.relayMx = relayCorrMatrix
        self.offset = offset
        self.magnetOffset = magnetOffset
        if board_num == 0:
            base_PV = 'ETOF:LV:{0:d}:ch:{1:d}:'.format(1,self.chan_num)
        if board_num == 1:
            base_PV = 'ETOF:LV:{0:d}:ch:{1:d}:'.format(3,self.chan_num)
        if board_num == 2:
            base_PV = 'ETOF:LV:{0:d}:ch:{1:d}:'.format(2,self.chan_num)
        self.imon = builder.aIn(base_PV+'imon')
        self.imon.LOPR = -0.5
        self.imon.HOPR = 3.5
        self.imon.LOW = 2.4
        self.imon.LOLO = 2.2
        self.imon.LSV ="MINOR"
        self.imon.LLSV = "MAJOR"

        prefix_PV = 'CBM:eTOF:LV:'
        #grab a channel status
        status_name = prefix_PV+'{0:d}:ch:{1:d}'.format(self.board_num,self.chan_num)+':onoff'
        self.status_PV = PV(status_name, callback=self.onStatusChange)

        #grab a current ADC value
        full_name = prefix_PV+'{0:d}:ch:{1:d}'.format(self.board_num,self.chan_num)+':volt'
        self.full_PV = PV(full_name, callback=self.onValueChange)        
        
        #grab magnetic field
        self.main_magnet_value = 4509.77
        self.pttEast2_value = 1329.43

        self.main_magnet = PV('cdev_mainMagnet2', callback=self.magnet_change)
        self.pttEast2 = PV('cdev_pttEast2', callback=self.poletip_change)
    #_____________________________________________________________________________                                
    def onStatusChange(self, pvname=None, value=None, **kws):
        if self.status_PV.value == 1: 
            self.pattern[self.board_num, self.chan_num - 1] = 1
        else:
            self.pattern[self.board_num, self.chan_num - 1] = 0

    #_____________________________________________________________________________
    def onValueChange(self, pvname=None, value=None, **kws):        
        offset = 13512.89 + np.dot(self.relayMx[self.chan_num - 1], self.pattern[self.board_num])
        #print(self.board_num, self.chan_num, self.magnetOffset[self.board_num, self.chan_num - 1])
        current_offset = self.offset[self.board_num, self.chan_num - 1]
        magnet_offset = (self.main_magnet_value +self.pttEast2_value)/5841*self.magnetOffset[self.board_num, self.chan_num - 1]
        revalue = (value - offset)/2090.54 - current_offset + magnet_offset         
        self.imon.set(revalue)
        #print(self.board_num, self.chan_num, revalue) 
    #_____________________________________________________________________________    
    def magnet_change(self, pvname=None, value=None, **kws):
        try:
            if abs(value) > 10000:
                self.main_magnet_value = 4509.77
            else:    
                self.main_magnet_value = value
        except:
             self.main_magnet_value = 4509.77
    def poletip_change(self, pvname=None, value=None, **kws):
        try:
            if abs(value) > 5000:
                self.pttEast2_value = 1329.43
            else:
                self.pttEast2_value = value
        except: 
            self.pttEast2_value = 1329.43
                
