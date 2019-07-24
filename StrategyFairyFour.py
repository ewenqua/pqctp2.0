#-*- coding:utf-8 -*-

import threading
from FinalLogger import logger
from Strategy import Strategy
from Indicators import Indicators
from Constant import *
from DatabaseController import DatabaseController

class StrategyFairyFour(threading.Thread, Strategy):
    def __init__(self, inst, volume = 1):
        Strategy.__init__(self, inst)
        threading.Thread.__init__(self)
        self.volume = volume
        self.InitIndicator()

    def InitIndicator(self):
        pass # no need to calculate indicator in this strategy

    def run(self):
        Strategy.strategy_state[self.tick['InstrumentID']] = True
        daybar_list = Indicators.getDayBarList(self.tick['InstrumentID'])
        if not daybar_list:
            print ('Need one bar at least in database')
            threading.Thread.__init__(self)
            Strategy.strategy_state[self.tick['InstrumentID']] = False
            return

        last_daybar = daybar_list[-1]
        #open, high, low, close, volume
        last_high = last_daybar[1]
        last_low = last_daybar[2]

        b_sendorder, s_sendorder = DatabaseController.getSendOrderCount(self.tick['InstrumentID'])

        if self.tick['LastPrice'] > last_high : # close short and open long
            if s_sendorder > 0 :
                self.PrepareOrder(self.tick['InstrumentID'], D_Buy, OF_Close, s_sendorder, self.tick['UpperLimitPrice']) # LastPrice
            elif b_sendorder < self.volume :
                self.PrepareOrder(self.tick['InstrumentID'], D_Buy, OF_Open, self.volume-b_sendorder, self.tick['UpperLimitPrice'])

        if self.tick['LastPrice'] < last_low : # close long and open short
            if b_sendorder > 0:
                self.PrepareOrder(self.tick['InstrumentID'], D_Sell, OF_Close, s_sendorder, self.tick['LowerLimitPrice'])  # LastPrice
            elif s_sendorder < self.volume :
                self.PrepareOrder(self.tick['InstrumentID'], D_Sell, OF_Open, self.volume-s_sendorder, self.tick['LowerLimitPrice'])

        # in case restart/reuse thread since python not support
        threading.Thread.__init__(self)
        Strategy.strategy_state[self.tick['InstrumentID']] = False

    def PrepareOrder(self, inst, direc, open_close, volume, price):
        order = self.formatOrder(inst, direc, open_close, volume, price)
        self.sendOrder(order)















