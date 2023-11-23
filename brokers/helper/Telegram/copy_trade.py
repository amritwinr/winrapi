from brokers.helper.finvasia.api_helper import ShoonyaApiPy
from telethon.sync import TelegramClient
import pandas as pd
import time
from datetime import datetime as dt, timedelta
import pytz
import asyncio
import os
from user.models import DnTelegramSubscribe
import datetime
import re
from rest_framework.response import Response


class TelegramBot:

    def __init__(self, account, finvasia_account, req):
        self.account = account
        self.req = req
        self.removed = set()
        self.filePath = './Files/'+account['phone']+'_'+req['name']+".txt"
        self.api = ShoonyaApiPy()

        self.api.set_session(
            userid=finvasia_account["userid"],
            password=finvasia_account["password"],
            usertoken=finvasia_account["access_token"]
        )

    def placeorder(self, date, text, tl_data):

        with open(self.filePath, 'a') as file:
            # Write some data to the file
            print("appended in file")
            file.write(str(date) + "\n")

        tl_msg = str(text)
        tl_msg = tl_msg.upper()

        dicts = {'NIFTY': 'NIFTY', 'BANKNIFTY': 'BANKNIFTY', 'MIDCP': 'MIDCPNIFTY', 'FINNIFTY': 'FINNIFTY', 'AARTIIND': 'AARTIIND', 'ABB': 'ABB', 'ABBOTINDIA': 'ABBOTINDIA', 'ABCAPITAL': 'ABCAPITAL', 'ABFRL': 'ABFRL', 'ACC': 'ACC', 'ADANIENT': 'ADANIENT', 'ADANIPORTS': 'ADANIPORTS', 'ALKEM': 'ALKEM', 'AMBUJACEM': 'AMBUJACEM', 'APOLLOHOSP': 'APOLLOHOSP', 'APOLLOTYRE': 'APOLLOTYRE', 'ASHOKLEY': 'ASHOKLEY', 'ASIANPAINT': 'ASIANPAINT', 'ASTRAL': 'ASTRAL', 'ATUL': 'ATUL', 'AUBANK': 'AUBANK', 'AUROPHARMA': 'AUROPHARMA', 'AXISBANK': 'AXISBANK', 'BAJAJ-AUTO': 'BAJAJ-AUTO', 'BAJAJFINSV': 'BAJAJFINSV', 'BAJFINANCE': 'BAJFINANCE', 'BALKRISIND': 'BALKRISIND', 'BALRAMCHIN': 'BALRAMCHIN', 'BANDHANBNK': 'BANDHANBNK', 'BANKBARODA': 'BANKBARODA', 'BATAINDIA': 'BATAINDIA', 'BEL': 'BEL', 'BERGEPAINT': 'BERGEPAINT', 'BHARATFORG': 'BHARATFORG', 'BHARTIARTL': 'BHARTIARTL', 'BHEL': 'BHEL', 'BIOCON': 'BIOCON', 'BOSCHLTD': 'BOSCHLTD', 'BPCL': 'BPCL', 'BRITANNIA': 'BRITANNIA', 'BSOFT': 'BSOFT', 'CANBK': 'CANBK', 'CANFINHOME': 'CANFINHOME', 'CHAMBLFERT': 'CHAMBLFERT', 'CHOLAFIN': 'CHOLAFIN', 'CIPLA': 'CIPLA', 'COALINDIA': 'COALINDIA', 'COFORGE': 'COFORGE', 'COLPAL': 'COLPAL', 'CONCOR': 'CONCOR', 'COROMANDEL': 'COROMANDEL', 'CROMPTON': 'CROMPTON', 'CUB': 'CUB', 'CUMMINSIND': 'CUMMINSIND', 'DABUR': 'DABUR', 'DALBHARAT': 'DALBHARAT', 'DEEPAKNTR': 'DEEPAKNTR', 'DELTACORP': 'DELTACORP', 'DIVISLAB': 'DIVISLAB', 'DIXON': 'DIXON', 'DLF': 'DLF', 'DRREDDY': 'DRREDDY', 'EICHERMOT': 'EICHERMOT', 'ESCORTS': 'ESCORTS', 'EXIDEIND': 'EXIDEIND', 'FEDERALBNK': 'FEDERALBNK', 'FSL': 'FSL', 'GAIL': 'GAIL', 'GLENMARK': 'GLENMARK', 'GMRINFRA': 'GMRINFRA', 'GNFC': 'GNFC', 'GODREJCP': 'GODREJCP', 'GODREJPROP': 'GODREJPROP', 'GRANULES': 'GRANULES', 'GRASIM': 'GRASIM', 'GSPL': 'GSPL', 'GUJGASLTD': 'GUJGASLTD', 'HAL': 'HAL', 'HAVELLS': 'HAVELLS', 'HCLTECH': 'HCLTECH', 'HDFCAMC': 'HDFCAMC', 'HDFCBANK': 'HDFCBANK', 'HDFCLIFE': 'HDFCLIFE', 'HEROMOTOCO': 'HEROMOTOCO', 'HINDALCO': 'HINDALCO', 'HINDCOPPER': 'HINDCOPPER', 'HINDPETRO': 'HINDPETRO', 'HINDUNILVR': 'HINDUNILVR', 'HONAUT': 'HONAUT', 'IBULHSGFIN': 'IBULHSGFIN', 'ICICIBANK': 'ICICIBANK',
                 'ICICIGI': 'ICICIGI', 'ICICIPRULI': 'ICICIPRULI', 'IDEA': 'IDEA', 'IDFC': 'IDFC', 'IDFCFIRSTB': 'IDFCFIRSTB', 'IEX': 'IEX', 'IGL': 'IGL', 'INDHOTEL': 'INDHOTEL', 'INDIACEM': 'INDIACEM', 'INDIAMART': 'INDIAMART', 'INDIGO': 'INDIGO', 'INDUSINDBK': 'INDUSINDBK', 'INDUSTOWER': 'INDUSTOWER', 'INFY': 'INFY', 'INTELLECT': 'INTELLECT', 'IOC': 'IOC', 'IPCALAB': 'IPCALAB', 'IRCTC': 'IRCTC', 'ITC': 'ITC', 'JINDALSTEL': 'JINDALSTEL', 'JKCEMENT': 'JKCEMENT', 'JSWSTEEL': 'JSWSTEEL', 'JUBLFOOD': 'JUBLFOOD', 'KOTAKBANK': 'KOTAKBANK', 'LALPATHLAB': 'LALPATHLAB', 'LAURUSLABS': 'LAURUSLABS', 'LICHSGFIN': 'LICHSGFIN', 'LT': 'LT', 'LTTS': 'LTTS', 'LUPIN': 'LUPIN', 'MANAPPURAM': 'MANAPPURAM', 'MARICO': 'MARICO', 'MARUTI': 'MARUTI', 'METROPOLIS': 'METROPOLIS', 'MFSL': 'MFSL', 'MGL': 'MGL', 'MSUMI': 'MOTHERSON', 'MPHASIS': 'MPHASIS', 'MRF': 'MRF', 'MUTHOOTFIN': 'MUTHOOTFIN', 'NAM-INDIA': 'NAM-INDIA', 'NATIONALUM': 'NATIONALUM', 'NAUKRI': 'NAUKRI', 'NAVINFLUOR': 'NAVINFLUOR', 'NESTLEIND': 'NESTLEIND', 'NMDC': 'NMDC', 'NTPC': 'NTPC', 'OBEROIRLTY': 'OBEROIRLTY', 'OFSS': 'OFSS', 'ONGC': 'ONGC', 'PAGEIND': 'PAGEIND', 'PEL': 'PEL', 'PERSISTENT': 'PERSISTENT', 'PETRONET': 'PETRONET', 'PFC': 'PFC', 'PIDILITIND': 'PIDILITIND', 'PIIND': 'PIIND', 'PNB': 'PNB', 'POLYCAB': 'POLYCAB', 'POWERGRID': 'POWERGRID', 'RAIN': 'RAIN', 'RAMCOCEM': 'RAMCOCEM', 'RBLBANK': 'RBLBANK', 'RECLTD': 'RECLTD', 'RELIANCE': 'RELIANCE', 'SAIL': 'SAIL', 'SBICARD': 'SBICARD', 'SBILIFE': 'SBILIFE', 'SBIN': 'SBIN', 'SHREECEM': 'SHREECEM', 'SIEMENS': 'SIEMENS', 'SRF': 'SRF', 'SUNPHARMA': 'SUNPHARMA', 'SUNTV': 'SUNTV', 'SYNGENE': 'SYNGENE', 'TATACHEM': 'TATACHEM', 'TATACOMM': 'TATACOMM', 'TATACONSUM': 'TATACONSUM', 'TATAMOTORS': 'TATAMOTORS', 'TATAPOWER': 'TATAPOWER', 'TATASTEEL': 'TATASTEEL', 'TCS': 'TCS', 'TECHM': 'TECHM', 'TITAN': 'TITAN', 'TORNTPHARM': 'TORNTPHARM', 'TORNTPOWER': 'TORNTPOWER', 'TRENT': 'TRENT', 'TVSMOTOR': 'TVSMOTOR', 'UBL': 'UBL', 'ULTRACEMCO': 'ULTRACEMCO', 'UPL': 'UBL', 'VEDL': 'VEDL', 'VOLTAS': 'VOLTAS', 'WHIRLPOOL': 'WHIRLPOOL', 'WIPRO': 'WIPRO', 'ZEEL': 'ZEEL', 'ZYDUSLIFE': 'ZYDUSLIFE'}

        lot = {'NIFTY': 50, "BANKNIFTY": 15, "MIDCP": 75, "FINNIFTY": 40}

        listData = tl_data["symbols"].split(',')
        listData = [word.strip() for word in listData]

        result = {}
        for key in listData:
            if key in dicts:
                result[key] = dicts[key]

        lot_result = {}
        for key in listData:
            if key in lot:
                lot_result[key] = lot[key]

        symbol = {"tsym": result}
        BUY_SELL = ["BUY", "SELL"]
        CE_PE = ["CE", "PE"]

        name_count = sum(1 for word in tl_msg.split()
                         if word in symbol["tsym"])
        LIST1 = [
            next((symbol["tsym"][word]
                 for word in tl_msg.split() if word in symbol["tsym"]), None)
        ] if name_count == 1 else ["Plz_write_one_name"]

        print({"name_count": name_count})
        print({"LIST1": LIST1})

        # #condition for index and stocks_option only
        if "Plz_write_one_name" not in LIST1 and any(word in LIST1 for word in LIST1) and any(word in tl_msg for word in BUY_SELL) and any(word in tl_msg for word in CE_PE):
            number_match = re.search(r'\d+', tl_msg)
            if number_match:
                number = number_match.group(0)
                print(f"first con. meet")
                print(LIST1)
                b_s = [word for word in tl_msg.split() if word in BUY_SELL][0]
                rdf = [{"CE": 0, "PE": 4}, {"CE": 0, "PE": 3}, {
                    "CE": 0, "PE": 2}, {"CE": 0, "PE": 1}] if LIST1[0] == 'FINNIFTY' else [{"CE": 0, "PE": 1}, {"CE": 0, "PE": 1}, {
                        "CE": 0, "PE": 1}, {"CE": 0, "PE": 1}]

                ce_pe = [word for word in tl_msg.split() if word in CE_PE][0]

                qty = lot[LIST1[0]]
                ATMStrike_ce = number

                def week_of_month(date):
                    first_day = date.replace(day=1)
                    adjusted_date = date - timedelta(days=date.day - 1)
                    week_number = (adjusted_date.weekday() + date.day - 1) // 7 + 1

                    if week_number == 5:
                        next_month = date.replace(day=28) + timedelta(days=4) 
                        next_month = next_month + timedelta(days=7 - next_month.weekday())
                        week_number = 1
                        return next_month, week_number

                    return date, week_number

                specific_date = datetime.today()
                result_date, week_number = week_of_month(specific_date)
                month_name = result_date.strftime('%b').upper()

                order = 0

                if order == 0:
                    try:
                        txt = (
                            f'{LIST1[0]} {month_name} {ATMStrike_ce}')
                        res = self.api.searchscrip('NFO', txt)
                        resDf = pd.DataFrame(res['values'])
                        resDf = resDf.sort_values(
                            by='dname').iloc[rdf[week_number-1][ce_pe]]

                        order = self.api.place_order(buy_or_sell='B', product_type='I',
                                                     exchange='NFO', tradingsymbol=resDf.tsym,
                                                     quantity=int(tl_data["quantity"]) * int(qty), discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                                     retention='DAY', remarks='my_order_001')

                        print({"order----": order})

                    except Exception as e:
                        print({"error": e})

        if "Plz_write_one_name" not in LIST1 and any(word in LIST1 for word in LIST1) and any(word in tl_msg for word in BUY_SELL) and not any(word in tl_msg for word in CE_PE):
            number_match = re.search(r'\d+', tl_msg)
            if not number_match:
                order = 0
                if order == 0:
                    try:
                        #     number = number_match.group(0)
                        #     print(f"second con. meet")
                        #     print(LIST1)
                        #     b_s = [word for word in tl_msg.split() if word in BUY_SELL][0]
                        #     print(number)

                        #     order = self.api.place_order(buy_or_sell= b_s[0], product_type='I',
                        # 				exchange='NSE', tradingsymbol=f"{LIST1[0]}-EQ",
                        # 				quantity=tl_data["quantity"], discloseqty=0,price_type='MKT', price=0, trigger_price=None,
                        # 				retention='DAY', remarks='my_order_001')
                        #     print({"order---": order})

                        # else:
                        print(f"second con. meet")
                        print(LIST1)
                        b_s = [word for word in tl_msg.split()
                               if word in BUY_SELL][0]

                        order = self.api.place_order(buy_or_sell=b_s[0], product_type='I',
                                                     exchange='NSE', tradingsymbol=f"{LIST1[0]}-EQ",
                                                     quantity=tl_data["quantity"], discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                                                     retention='DAY', remarks='my_order_001')
                        print({"order---": order})
                    except Exception as e:
                        print({"error": e})

    def trade(self):
        phone = self.account["phone"]

        symbols = self.req["symbols"]
        quantity = self.req["quantity"]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        chat = self.req["name"]

        while True:
            broker_creds_objects = DnTelegramSubscribe.objects.filter(
                id=self.req["id"])

            if broker_creds_objects.count() == 0:
                break

            with TelegramClient(os.path.abspath(self.account["phone"]), self.account["api_id"], self.account["api_hash"]) as client:
                self.df = pd.DataFrame(
                    columns=["group", "sender", "text", "date"])

                broker_creds_objects_list = list(
                    broker_creds_objects.values(
                        "quantity",
                        "name",
                        "symbols",
                    ),
                )

                tl_data = [
                    {
                        "quantity": str(acc['quantity']),
                        "name": str(acc['name']),
                        "symbols": str(acc['symbols']),
                    }
                    for acc in broker_creds_objects_list
                ]

                for message in client.iter_messages(chat, offset_date=dt.now() - timedelta(days=1), reverse=True, limit=None, wait_time=None):
                    data = {"group": chat, "sender": message.sender_id,
                            "text": message.text, "date": pd.to_datetime(message.date)}
                    temp_df = pd.DataFrame(data, index=[1])

                    date = message.date.astimezone(
                        pytz.timezone("Asia/Kolkata"))

                    self.df = pd.concat([self.df, temp_df], ignore_index=True)

                    if os.path.exists(self.filePath):
                        with open(self.filePath, 'r') as file:
                            for line in file:
                                self.removed.add(line.strip())

                    else:
                        with open(self.filePath, 'w') as f:
                            print("new file created")

                    if str(date) not in self.removed:
                        self.placeorder(date=date,
                                        text=message.text, tl_data=tl_data[0])

                    self.df['date'] = self.df['date'].apply(
                        lambda x: x.astimezone(pytz.timezone('Asia/Kolkata')))

            time.sleep(0.25)
