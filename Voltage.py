from softioc import builder, softioc
from epics import PV

class VOLTAGE():
    def __init__(self, board_num, chan_num):
        self.board_num = board_num
        self.chan_num = chan_num
        if board_num == 0:
            base_PV = 'ETOF:LV:{0:d}:ch:{1:d}:'.format(1,self.chan_num)
        if board_num == 1:
            base_PV = 'ETOF:LV:{0:d}:ch:{1:d}:'.format(3,self.chan_num)
        if board_num == 2:
            base_PV = 'ETOF:LV:{0:d}:ch:{1:d}:'.format(2,self.chan_num)
        self.vmon = builder.aIn(base_PV+'vmon')
        self.vmon.LOPR = 0
        self.vmon.HOPR = 15
        self.vmon.LOW = 11.7
        self.vmon.LOLO = 11.6
        self.vmon.LSV = "MINOR"
        self.vmon.LLSV = "MAJOR"
        
        prefix_PV = 'CBM:eTOF:LV:'
        full_name = prefix_PV+'{0:d}:ch:{1:d}'.format(self.board_num,self.chan_num)+':current'
        self.full_PV = PV(full_name,callback=self.onValueChange)        

    #_____________________________________________________________________________
    def onValueChange(self, pvname=None, value=None, **kws):
        revalue = (value - 6.25)/2034.29
        self.vmon.set(revalue)

