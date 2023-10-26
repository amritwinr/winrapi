from brokers.helper.finvasia.api_helper import ShoonyaApiPy
import pandas as pd
import pandas as pd
import math


class FinvaciaTradingBot:

    def __init__(self, accounts_finvasia, req):
        self.accounts_finvasia = accounts_finvasia
        self.req = req
        self.resDf = 0
        self.buy_sell = ""
        self.ATMStrike = 0

    def Buy(self):
        b_s = {
            "buy": "B",
            "sell": "S"
        }
        if self.req["buy_sell"]:
            self.buy_sell = b_s[self.req["buy_sell"]]

        api = ShoonyaApiPy()

        api.set_session(
            userid=self.accounts_finvasia["userid"],
            password=self.accounts_finvasia["password"],
            usertoken=self.accounts_finvasia["access_token"]
        )

        for_atm = {'NIFTY BANK': 100, 'AARTIIND': 10, 'ABB': 20, 'ABBOTINDIA': 250, 'ABCAPITAL': 2.5, 'ABFRL': 5, 'ACC': 20, 'ADANIENT': 50, 'ADANIPORTS': 10, 'ALKEM': 50, 'AMARAJABAT': 5, 'AMBUJACEM': 5, 'APOLLOHOSP': 50, 'APOLLOTYRE': 2.5, 'ASHOKLEY': 2.5, 'ASIANPAINT': 50, 'ASTRAL': 20, 'ATUL': 100, 'AUBANK': 10, 'AUROPHARMA': 10, 'AXISBANK': 10, 'BAJAJ_AUTO': 50, 'BAJAJFINSV': 250, 'BAJFINANCE': 100, 'BALKRISIND': 20, 'BALRAMCHIN': 10, 'BANDHANBNK': 5, 'BANKBARODA': 2.5, 'BATAINDIA': 20, 'BEL': 2.5, 'BERGEPAINT': 10, 'BHARATFORG': 10, 'BHARTIARTL': 10, 'BHEL': 1, 'BIOCON': 5, 'BOSCHLTD': 250, 'BPCL': 5, 'BRITANNIA': 20, 'BSOFT': 10, 'CANBK': 2.5, 'CANFINHOME': 10, 'CHAMBLFERT': 10, 'CHOLAFIN': 10, 'CIPLA': 10, 'COALINDIA': 2.5, 'COFORGE': 50, 'COLPAL': 10, 'CONCOR': 10, 'COROMANDEL': 10, 'CROMPTON': 5, 'CUB': 2.5, 'CUMMINSIND': 20, 'DABUR': 5, 'DALBHARAT': 20, 'DEEPAKNTR': 50, 'DELTACORP': 5, 'DIVISLAB': 50, 'DIXON': 50, 'DLF': 5, 'DRREDDY': 50, 'EICHERMOT': 20, 'ESCORTS': 20, 'EXIDEIND': 0.5, 'FEDERALBNK': 1, 'FSL': 2.5, 'GAIL': 2.5, 'GLENMARK': 5, 'GMRINFRA': 1, 'GNFC': 20, 'GODREJCP': 10, 'GODREJPROP': 20, 'GRANULES': 5, 'GRASIM': 20, 'GSPL': 5, 'GUJGASLTD': 10, 'HAL': 20, 'HAVELLS': 20, 'HCLTECH': 10, 'HDFC': 20, 'HDFCAMC': 20, 'HDFCBANK': 20, 'HDFCLIFE': 5, 'HEROMOTOCO': 20, 'HINDALCO': 5, 'HINDCOPPER': 2.5, 'HINDPETRO': 5, 'HINDUNILVR': 20, 'HONAUT': 500, 'IBULHSGFIN': 2.5, 'ICICIBANK': 10, 'ICICIGI': 20, 'ICICIPRULI': 5, 'IDEA': 1,
                   'IDFC': 1, 'IDFCFIRSTB': 1, 'IEX': 2.5, 'IGL': 5, 'INDHOTEL': 5, 'INDIACEM': 2.5, 'INDIAMART': 100, 'INDIGO': 20, 'INDUSINDBK': 10, 'INDUSTOWER': 2.5, 'INFY': 20, 'INTELLECT': 20, 'IOC': 0.65, 'IPCALAB': 10, 'IRCTC': 10, 'ITC': 2.5, 'JINDALSTEL': 10, 'JKCEMENT': 50, 'JSWSTEEL': 10, 'JUBLFOOD': 10, 'KOTAKBANK': 20, 'L_TFH': 1, 'LALPATHLAB': 50, 'LAURUSLABS': 10, 'LICHSGFIN': 5, 'LT': 20, 'LTTS': 50, 'LUPIN': 10, 'M_M': 10, 'M_MFIN': 2.5, 'MANAPPURAM': 1, 'MARICO': 5, 'MARUTI': 100, 'MCDOWELL-N': 10, 'METROPOLIS': 10, 'MFSL': 10, 'MGL': 10, 'MOTHERSON': 2.5, 'MPHASIS': 50, 'MRF': 500, 'MUTHOOTFIN': 20, 'NAM_INDIA': 5, 'NATIONALUM': 2.5, 'NAUKRI': 100, 'NAVINFLUOR': 50, 'NESTLEIND': 400, 'NMDC': 2.5, 'NTPC': 0.5, 'OBEROIRLTY': 20, 'OFSS': 50, 'ONGC': 2.5, 'PAGEIND': 500, 'PEL': 20, 'PERSISTENT': 50, 'PETRONET': 2.5, 'PFC': 1, 'PIDILITIND': 20, 'PIIND': 50, 'PNB': 1, 'POLYCAB': 50, 'POWERGRID': 2.5, 'PVR': 20, 'RAIN': 5, 'RAMCOCEM': 10, 'RBLBANK': 2.5, 'RECLTD': 1, 'RELIANCE': 20, 'SAIL': 1, 'SBICARD': 10, 'SBILIFE': 10, 'SBIN': 5, 'SHREECEM': 250, 'SIEMENS': 20, 'SRF': 50, 'SUNPHARMA': 10, 'SUNTV': 5, 'SYNGENE': 10, 'TATACHEM': 10, 'TATACOMM': 20, 'TATACONSUM': 10, 'TATAMOTORS': 10, 'TATAPOWER': 5, 'TATASTEEL': 2, 'TCS': 20, 'TECHM': 20, 'TITAN': 10, 'TORNTPHARM': 25, 'TORNTPOWER': 10, 'TRENT': 20, 'TVSMOTOR': 10, 'UBL': 20, 'ULTRACEMCO': 100, 'UPL': 10, 'VEDL': 5.5, 'VOLTAS': 20, 'WHIRLPOOL': 20, 'WIPRO': 5, 'ZEEL': 5, 'ZYDUSLIFE': 5}
        for_ltp = {'NIFTY BANK': 'Nifty Bank',
                   'AARTIIND': 'AARTIIND', 'ABB': 'ABB', 'ABBOTINDIA': 'ABBOTINDIA', 'ABCAPITAL': 'ABCAPITAL', 'ABFRL': 'ABFRL', 'ACC': 'ACC', 'ADANIENT': 'ADANIENT', 'ADANIPORTS': 'ADANIPORTS', 'ALKEM': 'ALKEM', 'AMARAJABAT': 'AMARAJABAT', 'AMBUJACEM': 'AMBUJACEM', 'APOLLOHOSP': 'APOLLOHOSP', 'APOLLOTYRE': 'APOLLOTYRE', 'ASHOKLEY': 'ASHOKLEY', 'ASIANPAINT': 'ASIANPAINT', 'ASTRAL': 'ASTRAL', 'ATUL': 'ATUL', 'AUBANK': 'AUBANK', 'AUROPHARMA': 'AUROPHARMA', 'AXISBANK': 'AXISBANK', 'BAJAJ-AUTO': 'BAJAJ-AUTO', 'BAJAJFINSV': 'BAJAJFINSV', 'BAJFINANCE': 'BAJFINANCE', 'BALKRISIND': 'BALKRISIND', 'BALRAMCHIN': 'BALRAMCHIN', 'BANDHANBNK': 'BANDHANBNK', 'BANKBARODA': 'BANKBARODA', 'BATAINDIA': 'BATAINDIA', 'BEL': 'BEL', 'BERGEPAINT': 'BERGEPAINT', 'BHARATFORG': 'BHARATFORG', 'BHARTIARTL': 'BHARTIARTL', 'BHEL': 'BHEL', 'BIOCON': 'BIOCON', 'BOSCHLTD': 'BOSCHLTD', 'BPCL': 'BPCL', 'BRITANNIA': 'BRITANNIA', 'BSOFT': 'BSOFT', 'CANBK': 'CANBK', 'CANFINHOME': 'CANFINHOME', 'CHAMBLFERT': 'CHAMBLFERT', 'CHOLAFIN': 'CHOLAFIN', 'CIPLA': 'CIPLA', 'COALINDIA': 'COALINDIA', 'COFORGE': 'COFORGE', 'COLPAL': 'COLPAL', 'CONCOR': 'CONCOR', 'COROMANDEL': 'COROMANDEL', 'CROMPTON': 'CROMPTON', 'CUB': 'CUB', 'CUMMINSIND': 'CUMMINSIND', 'DABUR': 'DABUR', 'DALBHARAT': 'DALBHARAT', 'DEEPAKNTR': 'DEEPAKNTR', 'DELTACORP': 'DELTACORP', 'DIVISLAB': 'DIVISLAB', 'DIXON': 'DIXON', 'DLF': 'DLF', 'DRREDDY': 'DRREDDY', 'EICHERMOT': 'EICHERMOT', 'ESCORTS': 'ESCORTS', 'EXIDEIND': 'EXIDEIND', 'FEDERALBNK': 'FEDERALBNK', 'FSL': 'FSL', 'GAIL': 'GAIL', 'GLENMARK': 'GLENMARK', 'GMRINFRA': 'GMRINFRA', 'GNFC': 'GNFC', 'GODREJCP': 'GODREJCP', 'GODREJPROP': 'GODREJPROP', 'GRANULES': 'GRANULES', 'GRASIM': 'GRASIM', 'GSPL': 'GSPL', 'GUJGASLTD': 'GUJGASLTD', 'HAL': 'HAL', 'HAVELLS': 'HAVELLS', 'HCLTECH': 'HCLTECH', 'HDFCAMC': 'HDFCAMC', 'HDFCBANK': 'HDFCBANK', 'HDFCLIFE': 'HDFCLIFE', 'HEROMOTOCO': 'HEROMOTOCO', 'HINDALCO': 'HINDALCO', 'HINDCOPPER': 'HINDCOPPER', 'HINDPETRO': 'HINDPETRO', 'HINDUNILVR': 'HINDUNILVR', 'HONAUT': 'HONAUT', 'IBULHSGFIN': 'IBULHSGFIN', 'ICICIBANK': 'ICICIBANK', 'ICICIGI': 'ICICIGI', 'ICICIPRULI': 'ICICIPRULI', 'IDEA': 'IDEA', 'IDFC': 'IDFC', 'IDFCFIRSTB': 'IDFCFIRSTB', 'IEX': 'IEX', 'IGL': 'IGL', 'INDHOTEL': 'INDHOTEL', 'INDIACEM': 'INDIACEM', 'INDIAMART': 'INDIAMART', 'INDIGO': 'INDIGO', 'INDUSINDBK': 'INDUSINDBK', 'INDUSTOWER': 'INDUSTOWER', 'INFY': 'INFY', 'INTELLECT': 'INTELLECT', 'IOC': 'IOC', 'IPCALAB': 'IPCALAB', 'IRCTC': 'IRCTC', 'ITC': 'ITC', 'JINDALSTEL': 'JINDALSTEL', 'JKCEMENT': 'JKCEMENT', 'JSWSTEEL': 'JSWSTEEL', 'JUBLFOOD': 'JUBLFOOD', 'KOTAKBANK': 'KOTAKBANK', 'LALPATHLAB': 'LALPATHLAB', 'LAURUSLABS': 'LAURUSLABS', 'LICHSGFIN': 'LICHSGFIN', 'LT': 'LT', 'LTTS': 'LTTS', 'LUPIN': 'LUPIN', 'MANAPPURAM': 'MANAPPURAM', 'MARICO': 'MARICO', 'MARUTI': 'MARUTI', 'METROPOLIS': 'METROPOLIS', 'MFSL': 'MFSL', 'MGL': 'MGL', 'MSUMI': 'MOTHERSON', 'MPHASIS': 'MPHASIS', 'MRF': 'MRF', 'MUTHOOTFIN': 'MUTHOOTFIN', 'NAM-INDIA': 'NAM-INDIA', 'NATIONALUM': 'NATIONALUM', 'NAUKRI': 'NAUKRI', 'NAVINFLUOR': 'NAVINFLUOR', 'NESTLEIND': 'NESTLEIND', 'NMDC': 'NMDC', 'NTPC': 'NTPC', 'OBEROIRLTY': 'OBEROIRLTY', 'OFSS': 'OFSS', 'ONGC': 'ONGC', 'PAGEIND': 'PAGEIND', 'PEL': 'PEL', 'PERSISTENT': 'PERSISTENT', 'PETRONET': 'PETRONET', 'PFC': 'PFC', 'PIDILITIND': 'PIDILITIND', 'PIIND': 'PIIND', 'PNB': 'PNB', 'POLYCAB': 'POLYCAB', 'POWERGRID': 'POWERGRID', 'RAIN': 'RAIN', 'RAMCOCEM': 'RAMCOCEM', 'RBLBANK': 'RBLBANK', 'RECLTD': 'RECLTD', 'RELIANCE': 'RELIANCE', 'SAIL': 'SAIL', 'SBICARD': 'SBICARD', 'SBILIFE': 'SBILIFE', 'SBIN': 'SBIN', 'SHREECEM': 'SHREECEM', 'SIEMENS': 'SIEMENS', 'SRF': 'SRF', 'SUNPHARMA': 'SUNPHARMA', 'SUNTV': 'SUNTV', 'SYNGENE': 'SYNGENE', 'TATACHEM': 'TATACHEM', 'TATACOMM': 'TATACOMM', 'TATACONSUM': 'TATACONSUM', 'TATAMOTORS': 'TATAMOTORS', 'TATAPOWER': 'TATAPOWER', 'TATASTEEL': 'TATASTEEL', 'TCS': 'TCS', 'TECHM': 'TECHM', 'TITAN': 'TITAN', 'TORNTPHARM': 'TORNTPHARM', 'TORNTPOWER': 'TORNTPOWER', 'TRENT': 'TRENT', 'TVSMOTOR': 'TVSMOTOR', 'UBL': 'UBL', 'ULTRACEMCO': 'ULTRACEMCO', 'UPL': 'UBL', 'VEDL': 'VEDL', 'VOLTAS': 'VOLTAS', 'WHIRLPOOL': 'WHIRLPOOL', 'WIPRO': 'WIPRO', 'ZEEL': 'ZEEL', 'ZYDUSLIFE': 'ZYDUSLIFE'}
        strike_ce = 0
        strike_pe = 0

        atm = for_atm[self.req["symbol"]]
        ltp = for_ltp[self.req["symbol"]]
        index_ltp = float(api.get_quotes('NSE', ltp)['lp'])

        if self.req["strike_type"] == "Auto":
            if self.buy_sell == "B":
                self.ATMStrike = math.ceil(index_ltp/atm)*atm+strike_ce*atm
            elif self.buy_sell == "S":
                self.ATMStrike = math.ceil(index_ltp/atm)*atm+strike_pe*atm

        else:
            if self.buy_sell == "B":
                self.ATMStrike = self.req["strike_ce"]
            else:
                self.ATMStrike = self.req["strike_pe"]

        if self.req["exchange"] == "NFO":
            month = self.req["expiry"]
            txt = (f'NIFTY BANK {month} {self.ATMStrike}')
            res = api.searchscrip('NFO', txt)
            resDf = pd.DataFrame(res['values'])
            # dname for monthly and weekly for week
            self.resDf = resDf.sort_values(by='dname').iloc[0]

        resDf = self.resDf.tsym if self.req["exchange"] == "NFO" else self.req["symbol"]
        order = api.place_order(buy_or_sell=self.buy_sell, product_type=self.req["market_type"],
                                exchange=self.req["exchange"], tradingsymbol=resDf,
                                quantity=self.req["quantity"], discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                retention='DAY', remarks='winralgo_tv')
        print(order)
