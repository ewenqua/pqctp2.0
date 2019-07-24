#-*- coding:utf-8 -*-

import threading
import time
from FinalLogger import logger
from DatabaseController import DatabaseController
from Constant import *
import sys
if sys.platform == 'win32':
    from ctp_win64.ctpwrapper import ApiStructure
elif sys.platform == 'linux':
    from ctp_linux64.ctpwrapper import ApiStructure

mutex = threading.Lock()

class Strategy():
    traderSpi = None #TraderApiPy()
    strategy_state = {}

    def __init__(self, inst):
        self.inst = inst

    def setTick(self, tick):
        self.tick = tick

    def InitIndicator(self):
        raise Exception('Implement Exception','InitInitcator should be implement for customized strategy!')

    @staticmethod
    def setTraderSpi(spi):
        Strategy.traderSpi = spi

    def sendOrder(self, order):
        global mutex
        mutex.acquire()

        Strategy.traderSpi.ReqOrderInsert(order, Strategy.traderSpi.inc_request_id())
        DatabaseController.insert_SendOrder(order.to_dict()) # dict will change bytes to str
        print ('sendOrder = ' + order.to_dict()['InstrumentID'] + ' dir = ' + order.to_dict()['Direction'] + ' price = '+ str(order.to_dict()['LimitPrice']) + ' strategy = ' + self.__module__)
        time.sleep(1)
        mutex.release()

    def formatOrder(self, inst, direc, open_close, volume, price):
        return ApiStructure.InputOrderField(
            InstrumentID=inst,
            BrokerID=Strategy.traderSpi.broker_id,
            Direction=direc, # D_Buy or D_Sell
            OrderRef=str(Strategy.traderSpi.inc_request_id()),
            LimitPrice=price,
            VolumeTotalOriginal=volume,
            OrderPriceType=OPT_LimitPrice,

            InvestorID=Strategy.traderSpi.investor_id,
            CombOffsetFlag=open_close, # OF_Open, OF_Close, OF_CloseToday
            CombHedgeFlag=HF_Speculation,
            ExchangeID=exchange_id[inst],
            VolumeCondition=VC_AV,
            MinVolume=1,
            ForceCloseReason=FCC_NotForceClose,
            IsAutoSuspend=1,
            UserForceClose=0,
            TimeCondition=TC_GFD,
            ContingentCondition=CC_Immediately
        )




