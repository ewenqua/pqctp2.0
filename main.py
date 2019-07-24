#-*- coding=utf-8 -*-
import sys
import getopt
import time
from MdApiPy import MdApiPy
from TraderApiPy import TraderApiPy
from TickController import TickController
from Strategy import Strategy
from StrategyRBreaker import StrategyRBreaker
from StrategyFairyFour import StrategyFairyFour
from StrategyDoubleMA import StrategyDoubleMA
from Constant import BROKER_ID,INVESTOR_ID,PASSWORD,AUTH_CODE,APP_ID,ADDR_MD,ADDR_TRADE,LOGS_DIR,inst_strategy,inst_thread

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def InitStrategy():
    for i in range(len(inst_strategy)):
        inst = list(inst_strategy.keys())[i]
        paras = inst_strategy[inst]   # paras = {'strategy':'StrategyFairyFour', 'MA20': 20, ...}
        #strategy = None
        if paras['strategy'] == 'StrategyRBreaker':
            inst_thread[inst] = StrategyRBreaker(inst, volume = paras['volume'])
        elif paras['strategy'] == 'StrategyFairyFour':
            inst_thread[inst] = StrategyFairyFour(inst)
        elif paras['strategy'] == 'StrategyDoubleMA':
            inst_thread[inst] = StrategyDoubleMA(inst,fast = paras['fast'],slow = paras['slow'], volume = paras['volume'])
        # add more strategy
        else:
            print ('The strategy is not found! ')
        inst_thread[inst].setDaemon(True)

def start():
    user_trade = TraderApiPy(broker_id=BROKER_ID, investor_id=INVESTOR_ID, passwd=PASSWORD, auth_code=AUTH_CODE,app_id=APP_ID)
    user_trade.Create(LOGS_DIR +"_trade")
    user_trade.RegisterFront(ADDR_TRADE)
    user_trade.Init()
    Strategy.setTraderSpi(user_trade)
    #print ('before init strategy')
    InitStrategy()

    user_md = MdApiPy(instruments=inst_strategy.keys(), broker_id=BROKER_ID, investor_id=INVESTOR_ID, passwd=PASSWORD)
    user_md.Create(LOGS_DIR +"_md")
    user_md.RegisterFront(ADDR_MD)
    user_md.Init()

    _date = '19700101'
    while True:
        time.sleep(60)
        _time = time.strftime('%H%M%S')
        hint_time = time.localtime(time.time())
        if hint_time.tm_min % 15 == 0:
            print ('The main thread is runing, date = %s, time = %s' % (time.strftime('%Y-%m-%d'),time.strftime('%H:%M:%S')))
        if '150000'< _time < '150100' and _date < time.strftime('%Y%m%d'):
            TickController.saveDayBar()
            _date = time.strftime('%Y%m%d')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error:
            raise Usage("opt error")
        #more code, unchanged
        for opt, value in opts:
            if opt in ("-h", "--help"):
                print ('please input null parameter to run.')
            elif opt in ("-t", "--test"):
                print ('not used, just test.')
        else:
            start()

    except Usage:
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())






