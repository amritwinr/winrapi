import pandas as pd
import math
from datetime import datetime, timedelta
class FinvasiaIndexLtpBot:

    def __init__(self, req, max_threads=50):

        self.max_threads = max_threads
        self.req = req

        # for finvasia
        self.sl_upper_b, self.sl_lower_b = 0, 0
        self.target_upper_b, self.target_lower_b = 0, 0
        self.bn_ltp, self.upper_ltp, self.lower_ltp = 0, 0, 0
        self.order = 0

        self.threshold = 1
        self.thresholdCE = 1
        self.thresholdPE = 1
        self.order_status = []
        self.order_placed_ce = "NO"
        self.order_placed_pe = "NO"
        self.traded_stocks_ce = []
        self.traded_stocks_pe = []
        self.ce_banknifty = []
        self.pe_banknifty = []
        self.banknifty_ce = []
        self.banknifty_pe = []

    def finvasia_indexLtp(self, api, atm, name, accounts_romil, indexLtp):
        upper_limit = float(accounts_romil["upper_level"])
        lower_limit = float(accounts_romil["lower_level"])

        strike_c = float(accounts_romil["strike_ce"])
        strike_p = float(accounts_romil["strike_pe"])
        target_up = float(accounts_romil["upper_target"])
        target_lo = float(accounts_romil["lower_target"])
        sl_up = float(accounts_romil["sl_upper"])
        sl_lo = float(accounts_romil["sl_lower"])

        ATMStrike_ce = math.ceil(indexLtp/atm)*atm+strike_c*atm
        ATMStrike_pe = math.ceil(indexLtp/atm)*atm+strike_p*atm
        month = self.req["expiry"]

        rdf = [{"CE": 0, "PE": 4}, { "CE": 0, "PE": 3 } , { "CE": 0, "PE": 2 }, { "CE": 0, "PE": 1 }] if name == "FIN NIFTY" else [{"CE": 0, "PE": 1}, {"CE": 0, "PE": 1}, {"CE": 0, "PE": 1}, {"CE": 0, "PE": 1}]

        def week_of_month(date):
            first_day = date.replace(day=1)
            adjusted_date = date - timedelta(days=date.day - 1)
            week_number = (adjusted_date.weekday() + date.day - 1) // 7 + 1

            if week_number > 4:
                next_month = date.replace(day=28) + timedelta(days=4) 
                next_month = next_month + timedelta(days=7 - next_month.weekday())
                week_number = 1
                return next_month, week_number

            return date, week_number

        specific_date = datetime.today()
        result_date, week_number = week_of_month(specific_date)

        if abs(upper_limit-indexLtp) <=1 and name not in self.traded_stocks_ce:
            print(f"{name} Upper range reached.")
            txt = (f'{name} {month} {ATMStrike_ce}')  # 15500'

            res = api.searchscrip('NFO', txt)
            resDf = pd.DataFrame(res['values'])
            resDf = resDf.sort_values(by='dname').iloc[0]

            order = api.place_order(buy_or_sell='B', product_type='I',
                                    exchange='NFO', tradingsymbol=resDf.tsym,
                                    quantity=self.req["quantity"], discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                    retention='DAY', remarks='my_order_001')
            print(order)

            self.traded_stocks_ce.append(name)
            self.ce_banknifty.append(resDf.tsym)
            self.target_upper_b = target_up+upper_limit
            self.sl_upper_b = upper_limit-sl_up
            self.order_placed_ce = "YES"


        if (self.order_placed_ce == "YES") and (indexLtp - self.sl_upper_b) <= self.threshold and (name not in self.banknifty_ce) or (self.order_placed_ce == "YES") and ((indexLtp - self.target_upper_b) >= self.threshold) and (name not in self.banknifty_ce):
            print(f"{name} Upper range exit reached.")

            order = api.place_order(buy_or_sell='S', product_type='I',
                                    exchange='NFO', tradingsymbol=self.ce_banknifty[0],
                                    quantity=self.req["quantity"], discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                    retention='DAY', remarks='my_order_001')
            print(order)
            self.banknifty_ce.append(name)

        if abs(indexLtp-lower_limit) <=1  and name not in self.traded_stocks_pe:
            print(f"{name} lower range reached.")
            txt = (f'{name} {month} {ATMStrike_pe}')  # 15500'
            res = api.searchscrip('NFO', txt)
            resDf = pd.DataFrame(res['values'])
            resDf = resDf.sort_values(by='dname').iloc[rdf[week_number-1]['PE']]

            order = api.place_order(buy_or_sell='B', product_type='I',
                                    exchange='NFO', tradingsymbol=resDf.tsym,
                                    quantity=self.req["quantity"], discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                    retention='DAY', remarks='my_order_001')
            print(order)

            self.traded_stocks_pe.append(name)
            self.pe_banknifty.append(resDf.tsym)
            self.order_placed_pe = "YES"
            self.target_lower_b = lower_limit-target_lo
            self.sl_lower_b = sl_lo+lower_limit

        if (self.order_placed_pe == "YES") and (indexLtp - self.sl_lower_b) >= self.threshold and (name not in self.banknifty_pe) or (self.order_placed_pe == "YES") and (indexLtp - self.target_lower_b) <= self.threshold and (name not in self.banknifty_pe):
            print("Bank Nifty Lower range exit reached.")

            order = api.place_order(buy_or_sell='S', product_type='I',
                                    exchange='NFO', tradingsymbol=self.pe_banknifty[0],
                                    quantity=self.req["quantity"], discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                    retention='DAY', remarks='my_order_001')
            print(order)
            self.banknifty_pe.append(name)

        flag = 0
        ram = 0
        for x in self.traded_stocks_ce:
            if (x == name):
                flag += 1
        for x in self.banknifty_ce:
            if (x == name):
                flag += 1
        for x in self.traded_stocks_pe:
            if (x == name):
                ram += 1
        for x in self.banknifty_pe:
            if (x == name):
                ram += 1
        if (flag == 2):
            self.traded_stocks_ce.remove(name)
            self.banknifty_ce.remove(name)
        if (ram == 2):
            self.traded_stocks_pe.remove(name)
            self.banknifty_pe.remove(name)
