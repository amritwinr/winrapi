import pandas as pd
import math
from datetime import datetime
from SmartApi import SmartConnect
import pyotp


class AngelIndexLtpBot:

    def __init__(self, req, max_threads=50):

        self.max_threads = max_threads
        self.req = req

        self.sl_upper_n, self.sl_lower_n = 0, 0
        self.target_upper_n, self.target_lower_n = 0, 0

        self.sl_upper_b, self.sl_lower_b = 0, 0
        self.target_upper_b, self.target_lower_b = 0, 0
        self.bn_ltp, self.upper_ltp, self.lower_ltp = 0, 0, 0
        self.order = 0

        self.order_placed_ce = "no"
        self.order_placed_pe = "no"
        self.order_status = []

        self.threshold = 1
        self.traded_stocks_ce = []
        self.traded_stocks_pe = []
        self.ce_banknifty = []
        self.pe_banknifty = []
        self.banknifty_ce = []
        self.banknifty_pe = []

    def angel_indexLtp(self, angel_account,  atm, symbol, accounts_romil, token_df, indexLtp):
        factor2 = pyotp.TOTP(angel_account["twoFA"]).now()
        obj = SmartConnect(api_key=angel_account["api_key"])
        data = obj.generateSession(
            angel_account["userid"], angel_account["password"], factor2)

        refreshToken = data['data']['refreshToken']
        feedToken = obj.getfeedToken()
        userProfile = obj.getProfile(refreshToken)
        print({"user" : userProfile})

        name = symbol

        expiry_day = datetime.strptime(
            accounts_romil["expiry"], '%Y-%m-%d').date()

        filtered_df = token_df[
            (token_df['name'] == symbol) &
            (token_df['instrumenttype'] == 'OPTIDX') &
            (token_df['expiry'] == expiry_day)
        ]

        upper_limit = float(accounts_romil["upper_level"])
        lower_limit = float(accounts_romil["lower_level"])

        print({"upper----": upper_limit})
        print({"lower----": lower_limit})
        print({"ce": self.traded_stocks_ce})
        print({"pe": self.traded_stocks_pe})

        strike_c = float(accounts_romil["strike_ce"])
        strike_p = float(accounts_romil["strike_pe"])
        target_up = float(accounts_romil["upper_target"])
        target_lo = float(accounts_romil["lower_target"])
        sl_up = float(accounts_romil["sl_upper"])
        sl_lo = float(accounts_romil["sl_lower"])
        Qty = int(accounts_romil["quantity"])

        def getTokenInfo(symbol, exch_seg='NSE', instrumenttype='OPTIDX', strike_price='', pe_ce='CE', expiry_day=None):
            df = filtered_df
            strike_price = strike_price*100
            if exch_seg == 'NSE':
                eq_df = df[(df['exch_seg'] == 'NSE')]
                return eq_df[eq_df['name'] == symbol]
            elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
                return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
            elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
                return df[(df['exch_seg'] == 'NFO') & (df['expiry'] == expiry_day) & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

        ATMStrike_ce = math.ceil(indexLtp/atm)*atm+strike_c*atm
        ATMStrike_pe = math.ceil(indexLtp/atm)*atm+strike_p*atm

        ce_strike = getTokenInfo(symbol, 'NFO', 'OPTIDX',
                                 ATMStrike_ce, 'CE', expiry_day).iloc[0]
        pe_strike = getTokenInfo(
            symbol, 'NFO', 'OPTIDX', ATMStrike_pe, 'PE', expiry_day).iloc[0]

        if indexLtp >= upper_limit and name not in self.traded_stocks_ce:
            print(f"{name} Upper range reached.")
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": ce_strike.symbol,
                "symboltoken": ce_strike.token,
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": Qty
            }

            orderId = obj.placeOrder(orderparams)
            print("The order id is: {} ".format(orderId))
            self.order_placed_ce = "yes"
            self.traded_stocks_ce.append(name)
            self.ce_banknifty.append(ce_strike)
            self.target_upper_b = target_up+upper_limit
            self.sl_upper_b = upper_limit-sl_up

        if (self.order_placed_ce == "YES") and (indexLtp - self.sl_upper_b) <= self.threshold and (name not in self.banknifty_ce) or (self.order_placed_ce == "YES") and ((indexLtp - self.target_upper_b) >= self.threshold) and (name not in self.banknifty_ce):
            print("{name} Upper range exit reached.")
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": self.ce_banknifty[0]['symbol'],
                "symboltoken": self.ce_banknifty[0]['token'],
                "transactiontype": "SELL",
                "exchange": "NFO",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": Qty
            }
            orderId = obj.placeOrder(orderparams)
            print("The order id is: {}".format(orderId))
            self.banknifty_ce.append(name)

        if indexLtp <= lower_limit and name not in self.traded_stocks_pe:
            print(f"{name} Lower range reached.")
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": pe_strike.symbol,
                "symboltoken": pe_strike.token,
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": Qty
            }
            orderId = obj.placeOrder(orderparams)
            print("The order id is: {}".format(orderId))
            self.order_placed_pe = "yes"
            self.traded_stocks_pe.append(name)
            self.pe_banknifty.append(pe_strike)
            self.target_lower_b = lower_limit-target_lo
            self.sl_lower_b = sl_lo+lower_limit

        if (self.order_placed_pe == "YES") and (indexLtp - self.sl_lower_b) >= self.threshold and (name not in self.banknifty_pe) or (self.order_placed_pe == "YES") and (indexLtp - self.target_lower_b) <= self.threshold and (name not in self.banknifty_pe):
            print("{name} Lower range exit reached.")
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": self.pe_banknifty[0]['symbol'],
                "symboltoken": self.pe_banknifty[0]['token'],
                "transactiontype": "SELL",
                "exchange": "NFO",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": Qty
            }
            orderId = obj.placeOrder(orderparams)
            print("The order id is: {}".format(orderId))
            self.banknifty_pe.append(name)
