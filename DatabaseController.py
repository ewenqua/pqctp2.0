#-*- coding:utf-8 -*-
import sqlite3
import time
from FinalLogger import logger
from Constant import *

conn = sqlite3.connect('futures.db3', check_same_thread = False)
# init database and read data to memory
for i in inst_strategy.keys() :
    # create table if not exist
    cmd = "CREATE TABLE IF NOT EXISTS " + i + suffix_list[0]\
          + " (id INTEGER PRIMARY KEY NULL, inst TEXT NULL, open DOUBLE NULL, high DOUBLE NULL, low DOUBLE NULL, close DOUBLE NULL, volume INTEGER NULL, TradingDay TEXT NULL, time TEXT NULL)"
    conn.execute(cmd)

    cmd = "CREATE TABLE IF NOT EXISTS " + i + suffix_list[1] \
          + " (id INTEGER PRIMARY KEY NULL, inst TEXT NULL, OrderRef TEXT NULL, Direction TEXT NULL, OffsetFlag TEXT NULL, Price DOUBLE NULL, Volume INTEGER NULL, TradeDate TEXT NULL, TradeTime TIME NULL )"
    conn.execute(cmd)

    cmd = "CREATE TABLE IF NOT EXISTS " + i + suffix_list[2] \
          + " (id INTEGER PRIMARY KEY NULL, inst TEXT NULL, OrderRef TEXT NULL, Direction TEXT NULL, OffsetFlag TEXT NULL, Price DOUBLE NULL, Volume INTEGER NULL, TradeDate TEXT NULL, TradeTime TIME NULL )"
    conn.execute(cmd)

    # [xx_DayBar[], xx_SendOrder[], xx_RtnOrder[]]
    table_list = []

    cursor = conn.execute("SELECT open, high, low, close, volume from %s WHERE inst='%s'" % (i + suffix_list[0], i))
    day_bar = cursor.fetchall()
    if day_bar is not None :
        d = list(day_bar)
        table_list.append(d)

    cursor = conn.execute("SELECT OrderRef, Direction, OffsetFlag, Price, Volume from %s WHERE inst='%s'" % (i + suffix_list[1], i))
    send_order = cursor.fetchall()
    if send_order is not None:
        s = list(send_order)
        table_list.append(s)

    cursor = conn.execute("SELECT OrderRef, Direction, OffsetFlag, Price, Volume from %s WHERE inst='%s'" % (i + suffix_list[2], i))
    rtn_order = cursor.fetchall()
    if rtn_order is not None :
        r = list(rtn_order)
        table_list.append(r)

    database_map[i] = table_list

class DatabaseController():
    def __init__(self):
        pass
    @staticmethod
    def insert_DayBar(tick):
        try:
            conn.execute("INSERT INTO %s (inst, open, high, low, close, volume, TradingDay,time) VALUES ('%s', %f, %f, %f, %f, %d, '%s','%s')"
                         % (tick['InstrumentID'] + suffix_list[0], tick['InstrumentID'], tick['OpenPrice'], tick['HighestPrice'], tick['LowestPrice'], tick['LastPrice'], tick['Volume'], tick['TradingDay'],tick['UpdateTime']))
            conn.commit()
            #sync memory and database
            #[0] - DayBar [1] - SendOrder [2] - RtnOrder
            database_map[tick['InstrumentID']][0].append((tick['OpenPrice'], tick['HighestPrice'], tick['LowestPrice'], tick['LastPrice'], tick['Volume']))
        except sqlite3.OperationalError as e:
            print(e)
        except Exception as e:
            print('except in insert_DayBar:' + str(e))
    @staticmethod
    def insert_SendOrder(pInputOrder):
        try:
            conn.execute("INSERT INTO %s (inst, OrderRef, Direction, OffsetFlag, Price, Volume, TradeDate, TradeTime) VALUES ('%s','%s','%s','%s',%f, %d,'%s','%s')"
                         % (pInputOrder['InstrumentID']+suffix_list[1], pInputOrder['InstrumentID'], pInputOrder['OrderRef'], pInputOrder['Direction'], pInputOrder['CombOffsetFlag'], pInputOrder['LimitPrice'], pInputOrder['VolumeTotalOriginal'], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S")))
            conn.commit()
            #sync memory and database
            # [0] - DayBar [1] - SendOrder [2] - RtnOrder
            database_map[pInputOrder['InstrumentID']][1].append((pInputOrder['OrderRef'], pInputOrder['Direction'], pInputOrder['CombOffsetFlag'], pInputOrder['LimitPrice'], pInputOrder['VolumeTotalOriginal']))
        except sqlite3.OperationalError as e:
            print(e)
        except Exception as e:
            print('except in insert_SendOrder:' + str(e))
    @staticmethod
    def insert_RtnOrder(pTrade):
        #print('insert_RtnOrder: ' + str(pTrade))
        try:
            send_pos_buy, send_pos_sell = DatabaseController.getSendOrderCount(pTrade['InstrumentID'])
            rtn_pos_buy, rtn_pos_sell = DatabaseController.getRtnOrderCount(pTrade['InstrumentID'])
            #print('send_pos_buy %d send_pos_sell %d rtn_pos_buy %d rtn_pos_sell %d ' % (send_pos_buy ,send_pos_sell ,rtn_pos_buy , rtn_pos_sell))

            if (pTrade['Direction'] == D_Buy and send_pos_buy <= rtn_pos_buy) or (pTrade['Direction'] == D_Sell and send_pos_sell <= rtn_pos_sell):
                print('Maybe send order by human : ' + str(pTrade))
                return

            conn.execute("INSERT INTO %s (inst, OrderRef, Direction, OffsetFlag, Price, Volume, TradeDate, TradeTime) VALUES ('%s','%s', '%s', '%s', %f, %d, '%s','%s')"
                         % (pTrade['InstrumentID']+suffix_list[2], pTrade['InstrumentID'], pTrade['OrderRef'], pTrade['Direction'], pTrade['OffsetFlag'], pTrade['Price'], pTrade['Volume'], pTrade['TradeDate'], pTrade['TradeTime']))
            conn.commit()
            # sync memory and database
            # [0] - DayBar [1] - SendOrder [2] - RtnOrder
            database_map[pTrade['InstrumentID']][2].append(
                (pTrade['OrderRef'], pTrade['Direction'], pTrade['OffsetFlag'], pTrade['Price'], pTrade['Volume']))
        except sqlite3.OperationalError as e:
            print(e)
        except Exception as e:
            print('except in insert_RtnOrder:' + str(e))

    @staticmethod
    def getSendOrderCount(inst):
        sendorder_list = database_map[inst][suffix_list.index('_SendOrder')]
        pos_buy, pos_sell = (0, 0)
        for sendorder in sendorder_list:
            if sendorder[1] == D_Buy and sendorder[2] == OF_Open:
                pos_buy += sendorder[4]
            if sendorder[1] == D_Sell and sendorder[2] == OF_Open:
                pos_sell += sendorder[4]
            if sendorder[1] == D_Sell and sendorder[2] == OF_Close:
                pos_buy -= sendorder[4]
            if sendorder[1] == D_Buy and sendorder[2] == OF_Close:
                pos_sell -= sendorder[4]
        return pos_buy, pos_sell

    @staticmethod
    def getRtnOrderCount(inst):
        sendorder_list = database_map[inst][suffix_list.index('_RtnOrder')]
        pos_buy, pos_sell = (0, 0)
        for sendorder in sendorder_list:
            if sendorder[1] == D_Buy and sendorder[2] == OF_Open:
                pos_buy += sendorder[4]
            if sendorder[1] == D_Sell and sendorder[2] == OF_Open:
                pos_sell += sendorder[4]
            if sendorder[1] == D_Sell and sendorder[2] == OF_Close:
                pos_buy -= sendorder[4]
            if sendorder[1] == D_Buy and sendorder[2] == OF_Close:
                pos_sell -= sendorder[4]
        return pos_buy, pos_sell

if __name__ == "__main__":
    pass


