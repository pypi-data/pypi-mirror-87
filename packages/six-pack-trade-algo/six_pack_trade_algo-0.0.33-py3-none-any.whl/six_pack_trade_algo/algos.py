import pandas as pd
import ta
from ta.utils import dropna
from datetime import datetime, timedelta
import time
import pickle
import heapq

try:
    from .util import AlgoLogger
except:
    from util import AlgoLogger
#
#
#       Classes in algos
#
#           Algo
#           AlgoRsiBb
#


class Algo:
    def __init__(self, order_manager, data_path, data_source, GUID, config):
        self.log = AlgoLogger(data_path=data_path)
        self.log.set_name(GUID)
        self.data_source = data_source
        self.GUID = GUID
        self.orders = []
        self.positions = {}
        self.tick_period = int(config["tick_period"])       # the interval of the algo in seconds.
                                                            # if its run every day, the interval is 86400, for example
        order_manager.log = self.log
        self.order_manager = order_manager
        self.tickers = order_manager.tickers

    def run(self):
        self.log.info("STARTED ALGO:  " + self.GUID)
        if not bool(self.data_source.get_clock()["is_open"]):
            self.log.warn("Market is closed")
        else:
            self.log.info("Market is open")
        self.order_manager.load_algo()
        self.log.output()

    def run_end(self):
        self.log.info("Market is closed. Saving wallet data...")
        self.order_manager.save_algo()
        self.log.output()

    def print_details(self):
        return ""


class AlgoRsiBb(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,  config)
        self.data_points = int(config["data_points"])
        self.stddev = float(config["std_dev"])
        self.rsi_high = float(config["rsi_high"])
        self.rsi_low = float(config["rsi_low"])
        self.bollinger_indicator = {}
        for t in self.tickers:
            self.bollinger_indicator[t] = "Middle"

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.tickers:
                try:
                    trades[t] += [self.data_source.get_last_trade(t)["price"]]
                except Exception as e:
                    trades[t] = [self.data_source.get_last_trade(t)["price"]]
                try:
                    if len(trades[t]) > self.data_points:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        rsi = self.generateRsiIndicator(trades_df['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands, rsi)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/self.data_points))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.positions)


    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.data_points, ndev=self.stddev)
        return bollingerBands

    def generateRsiIndicator(self, df):
        rsi = ta.momentum.rsi(df, n = self.data_points)
        return rsi

    def trade(self, ticker, bollingerBands, rsi):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is above bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Above"
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is below bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Below"
        else:
            self.log.info("Current RSI_BB: {}  is inbetween bollinger bands; Checking RSIs : {} ".format(ticker, rsi.tail(1).iloc[0]))
            if ((rsi.tail(1).iloc[0] > 50) and (self.bollinger_indicator[ticker] == "Below")) or (rsi.tail(1).iloc[0] > self.rsi_high):
                self.order_manager.buy_shares(ticker)
            elif ((rsi.tail(1).iloc[0] < 50) and (self.bollinger_indicator[ticker] == "Above")) or (rsi.tail(1).iloc[0] > self.rsi_low):
                self.order_manager.sell_proportional(ticker)
            self.bollinger_indicator[ticker] = "Middle"
            
    def print_details(self):
        return "{}, {}, {}, {}".format(self.data_points, self.stddev, self.rsi_high, self.rsi_low)

class AlgoMeanReversionBuckets(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,  config)
        self.data_points = int(config["data_points"])
        self.stddev = float(config["std_dev"])
        self.rsi_high = float(config["rsi_high"])
        self.rsi_low = float(config["rsi_low"])
        self.bollinger_indicator = {}
        for t in self.tickers:
            self.bollinger_indicator[t] = "Middle"

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.tickers:
                try:
                    trades[t] += [self.data_source.get_last_trade(t)["price"]]
                except Exception as e:
                    trades[t] = [self.data_source.get_last_trade(t)["price"]]
                try:
                    if len(trades[t]) > self.data_points:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        rsi = self.generateRsiIndicator(trades_df['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands, rsi)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/self.data_points))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.positions)

    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.data_points, ndev=self.stddev)
        return bollingerBands

    def generateRsiIndicator(self, df):
        rsi = ta.momentum.rsi(df, n = self.data_points)
        return rsi

    def trade(self, ticker, bollingerBands, rsi):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is above bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Above"
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is below bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Below"
        else:
            self.log.info("Current RSI_BB: {}  is inbetween bollinger bands; Checking RSIs : {} ".format(ticker, rsi.tail(1).iloc[0]))
            if ((rsi.tail(1).iloc[0] > 50) and (self.bollinger_indicator[ticker] == "Below")) or (rsi.tail(1).iloc[0] > self.rsi_high):
                self.order_manager.buy_shares(ticker)
            elif ((rsi.tail(1).iloc[0] < 50) and (self.bollinger_indicator[ticker] == "Above")) or (rsi.tail(1).iloc[0] > self.rsi_low):
                self.order_manager.sell_proportional(ticker)
            self.bollinger_indicator[ticker] = "Middle"
            
    def print_details(self):
        return "{}, {}, {}, {}".format(self.data_points, self.stddev, self.rsi_high, self.rsi_low)

class AlgoRebalancing(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,config)
        self.ran_today = False
        
    def run(self, return_dict):
        super().run()
        # while bool(self.data_source.get_clock()["is_open"]):
        run_once = True
        while run_once:
            # if self.data_source.get_date():
            #     continue
            # else:
            #     self.ran_today = True
            proportions = []
            equity = self.order_manager.get_total_value() * .95 # set aside 5 % at all times
            for t in self.tickers:
                proportions.append(1.0/len(self.tickers))

            to_buy = []
            to_sell = []
            for i, t in enumerate(self.tickers):
                self.log.info("Rebalancing " + t)
                desired_value = proportions[i] * equity
                
                current_pos = self.data_source.get_position(t)
                # print(current_pos)
                current_value = float(current_pos["market_value"])
                current_share_price = float(current_pos["current_price"])
                if current_share_price == 0:
                    current_share_price = self.data_source.get_last_trade(t)["price"]
                
                # first I want to sell.
                # then i want to buy
                self.log.info("Desired : {},   Current : {},     Share Price : {}".format(desired_value, current_value, current_share_price))
                
                if desired_value == current_value:
                    continue
                if desired_value > current_value:
                    shares_to_buy = int((desired_value-current_value)/current_share_price)
                    if shares_to_buy != 0:
                        to_buy.append((t,shares_to_buy,current_share_price))
                    else:
                        self.log.info("Not enough of a difference to buy another share")
                if desired_value < current_value:
                    shares_to_sell = int((current_value-desired_value)/current_share_price)
                    if shares_to_sell != 0:
                        to_sell.append((t,shares_to_sell,current_share_price))
                    else:
                        self.log.info("Not enough of a difference to sell another share")
                        
            self.order_manager.rebalance(to_sell, to_buy)
            
            self.log.output()
            self.data_source.quick_test = True
            self.data_source.step(self.tick_period)
            run_once = False
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.positions)

class AlgoFactory():
    def __init__(self, type="RSI_BB"):
        self.type = type
        
    def build(self, order_manager, data_path, data_source, GUID, config):
        if self.type == "RSI_BB":
            return AlgoRsiBb(
                order_manager=order_manager,
                data_path=data_path,
                data_source=data_source,
                GUID=GUID,
                config=config
                )
        if self.type == "REBALANCING":
            return AlgoRebalancing(
                order_manager=order_manager,
                data_path=data_path,
                data_source=data_source,
                GUID=GUID,
                config=config
                )
        return
        
    def setType(self, type):
        self.type = type
    