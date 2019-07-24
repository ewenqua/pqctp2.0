#-*- coding=utf-8 -*-
#one inst -> one strategy/thread, and customized indicators
inst_strategy = {'c2001': {'strategy':'StrategyRBreaker', 'volume':3},
                 'rb2001': {'strategy':'StrategyFairyFour'},
                 'SR001': {'strategy':'StrategyDoubleMA', 'fast':7,'slow':30, 'volume':2},
                 }
#上海期货交易所 SHFE 大连商品交易所 DCE 郑州商品交易所 CZCE 中国金融期货交易所(CFFEX) 中国国际能源交易所(INE)
exchange_id = {'rb2001':'SHFE', 'c2001':'DCE', 'SR001':'CZCE'}

#{'p2001', strategy_thread}
inst_thread = {}

# {'inst', [DayBar, SendOrder, RtnOrder]}
#             |_____[ bar1, bar2, bar3, ...]
#                      |_____(open, high, low, close, ...)
database_map = {}
suffix_list = ['_DayBar', '_SendOrder', '_RtnOrder']

#仿真
BROKER_ID = "9999"
INVESTOR_ID = "142312"
PASSWORD = "pqctp2.0"
AUTH_CODE = "0000000000000000"
APP_ID = "simnow_client_test"
ADDR_MD = "tcp://180.168.146.187:10111"
ADDR_TRADE = "tcp://180.168.146.187:10101"

TICK_DIR = './ticks/'
LOGS_DIR = './logs/'

OPEN,HIGH,LOW,CLOSE = range(4)

#买卖方向
D_Buy = '0' #买
D_Sell = '1' #卖

#开平标志
OF_Open = '0' #开仓
OF_Close = '1' #平仓
OF_ForceClose = '2' #强平
OF_CloseToday = '3' #平今
OF_CloseYesterday = '4' #平昨
OF_ForceOff = '5' #强减
OF_LocalForceClose = '6' #本地强平

#报单价格条件
OPT_AnyPrice = '1' #任意价
OPT_LimitPrice = '2' #限价
OPT_BestPrice = '3' #最优价
OPT_LastPrice = '4' #最新价
OPT_LastPricePlusOneTicks = '5' #最新价浮动上浮1个ticks
OPT_LastPricePlusTwoTicks = '6' #最新价浮动上浮2个ticks
OPT_LastPricePlusThreeTicks = '7' #最新价浮动上浮3个ticks
OPT_AskPrice1 = '8' #卖一价
OPT_AskPrice1PlusOneTicks = '9' #卖一价浮动上浮1个ticks
OPT_AskPrice1PlusTwoTicks = 'A' #卖一价浮动上浮2个ticks
OPT_AskPrice1PlusThreeTicks = 'B' #卖一价浮动上浮3个ticks
OPT_BidPrice1 = 'C' #买一价
OPT_BidPrice1PlusOneTicks = 'D' #买一价浮动上浮1个ticks
OPT_BidPrice1PlusTwoTicks = 'E' #买一价浮动上浮2个ticks
OPT_BidPrice1PlusThreeTicks = 'F' #买一价浮动上浮3个ticks
OPT_FiveLevelPrice = 'G' #五档价

#投机套保标志
HF_Speculation = '1' #投机
HF_Arbitrage = '2' #套利
HF_Hedge = '3' #套保

#成交量类型
VC_AV = '1' #任何数量
VC_MV = '2' #最小数量
VC_CV = '3' #全部数量

#强平原因
FCC_NotForceClose = '0' #非强平
FCC_LackDeposit = '1' #资金不足
FCC_ClientOverPositionLimit = '2' #客户超仓
FCC_MemberOverPositionLimit = '3' #会员超仓
FCC_NotMultiple = '4' #持仓非整数倍
FCC_Violation = '5' #违规
FCC_Other = '6' #其它
FCC_PersonDeliv = '7' #自然人临近交割

#有效期类型
TC_IOC = '1' #立即完成，否则撤销
TC_GFS = '2' #本节有效
TC_GFD = '3' #当日有效
TC_GTD = '4' #指定日期前有效
TC_GTC = '5' #撤销前有效
TC_GFA = '6' #集合竞价有效

#触发条件
CC_Immediately = '1' #立即
CC_Touch = '2' #止损
CC_TouchProfit = '3' #止赢
CC_ParkedOrder = '4' #预埋单
CC_LastPriceGreaterThanStopPrice = '5' #最新价大于条件价
CC_LastPriceGreaterEqualStopPrice = '6' #最新价大于等于条件价
CC_LastPriceLesserThanStopPrice = '7' #最新价小于条件价
CC_LastPriceLesserEqualStopPrice = '8' #最新价小于等于条件价
CC_AskPriceGreaterThanStopPrice = '9' #卖一价大于条件价
CC_AskPriceGreaterEqualStopPrice = 'A' #卖一价大于等于条件价
CC_AskPriceLesserThanStopPrice = 'B' #卖一价小于条件价
CC_AskPriceLesserEqualStopPrice = 'C' #卖一价小于等于条件价
CC_BidPriceGreaterThanStopPrice = 'D' #买一价大于条件价
CC_BidPriceGreaterEqualStopPrice = 'E' #买一价大于等于条件价
CC_BidPriceLesserThanStopPrice = 'F' #买一价小于条件价
CC_BidPriceLesserEqualStopPrice = 'H' #买一价小于等于条件价




