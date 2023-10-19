from .api_helper import ShoonyaApiPy
from SmartApi import SmartConnect
import requests
import pandas as pd
import time
import warnings
import os
import pyotp
import pdb
from datetime import datetime, date
import math
from django.db.models import F

from user.models import DnRomilBroker
from brokers.helper.finvasia.romil_finvasia import FinvasiaIndexLtpBot
from brokers.helper.angelone.romil_angel import AngelIndexLtpBot


class AngelRomilBot:

    def __init__(self, angel_account, finvasia_account, other_accounts, logger, req, max_threads=50):
        self.logger = logger
        self.angel_account = angel_account
        self.finvasia_account = finvasia_account
        self.accounts = other_accounts
        self.max_threads = max_threads
        self.req = req
        self.indexLtpGlobal = float(0)
        self.finBot = FinvasiaIndexLtpBot(
                req=self.req)
        self.angelBot = AngelIndexLtpBot(
                req=self.req)

    def process_orders(self):
        api = ShoonyaApiPy()

        api.set_session(
            userid=self.finvasia_account["userid"],
            password=self.finvasia_account["password"],
            usertoken=self.finvasia_account["access_token"]
        )

        factor2 = pyotp.TOTP(self.angel_account["twoFA"]).now()
        obj = SmartConnect(api_key=self.angel_account["api_key"])
        data = obj.generateSession(
            self.angel_account["userid"], self.angel_account["password"], factor2)
        
        refreshToken= data['data']['refreshToken']
        feedToken=obj.getfeedToken()
        userProfile= obj.getProfile(refreshToken)

        url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
        data = requests.get(url).json()
        token_df = pd.DataFrame.from_dict(data)
        token_df['expiry'] = pd.to_datetime(token_df['expiry']).dt.date
        token_df = token_df.astype({'strike': float})

        finvasia_lists = [
            d for d in self.accounts if d.get('type') == "Finvasia"]

        angel_lists = [
            d for d in self.accounts if d.get('type') == "Angel One"]

        fin_symbols = [d['symbol'] for d in finvasia_lists]
        angel_symbols = [d['symbol'] for d in angel_lists]

        indexFin = None
        indexAngel = None

        if (self.req["type"] == "Finvasia"):
            indexFin = fin_symbols.index(self.req["symbol"])
            indexAngel = fin_symbols.index(self.req["symbol"])

        elif (self.req["type"] == "Angel One"):
            indexAngel = angel_symbols.index(self.req["symbol"])
            indexFin = angel_symbols.index(self.req["symbol"])

        watchlist = ['NIFTY 50']
        watchlist2 = ['NIFTY']
        watchlist1 = list(watchlist)  # Convert watchlist1 to a list

        watchDictFin = {
            'NIFTY': fin_symbols[0],
            'BANKNIFTY': fin_symbols[1],
            'FINNIFTY': fin_symbols[2],
            'MIDCAPNIFTY': fin_symbols[3],
        }

        watchDictAngel = {
            'NIFTY': angel_symbols[0],
            'NIFTY': angel_symbols[0],
            'NIFTY': angel_symbols[0],
            'NIFTY': angel_symbols[0],
        }

        filtered_dict_fin = {}
        filtered_dict_angel = {}

        # Check if the name matches any key in my_dict
        for key, value in watchDictFin.items():
            if value == fin_symbols[indexFin]:
                filtered_dict_fin[key] = value

        for key, value in watchDictAngel.items():
            if value == angel_symbols[indexAngel]:
                filtered_dict_angel[key] = value

        # Create a dictionary with your watchlists
        for_ltp = {
            tuple(watchlist1): filtered_dict_fin,
            tuple(watchlist2): filtered_dict_angel
        }

        for_atm = {'NIFTY BANK': 100, 'NIFTY': 50, 'NIFTY 50': 50}

        while True:
            broker_creds_objects = DnRomilBroker.objects.filter(
                id=self.req["id"])

            broker_creds_objects_list = list(
                broker_creds_objects.values(
                    "id",
                    "upper_level",
                    "lower_level",
                    "upper_target",
                    "lower_target",
                    "sl_upper",
                    "sl_lower",
                    "strike_ce",
                    "strike_pe",
                    "quantity",
                    "expiry",
                    "type",
                    "symbol",
                    "status"
                ),
            )

            accounts_romil = [
                {
                    "id": str(acc['id']),
                    "upper_level": str(acc['upper_level']),
                    "lower_level": str(acc['lower_level']),
                    "upper_target": str(acc['upper_target']),
                    "lower_target": str(acc["lower_target"]),
                    "sl_upper": str(acc["sl_upper"]),
                    "sl_lower": str(acc["sl_lower"]),
                    "strike_ce": str(acc["strike_ce"]),
                    "strike_pe": str(acc["strike_pe"]),
                    "quantity": str(acc["quantity"]),
                    "expiry": str(acc["expiry"]),
                    "type": str(acc["type"]),
                    "symbol": str(acc["symbol"]),
                    "status": str(acc["status"]),
                }
                for acc in broker_creds_objects_list
            ]

            if accounts_romil[0]["status"] == '0':
                break

            for name in watchlist1 + watchlist2:
                atm = for_atm[name]

                ltp = for_ltp.get(tuple(watchlist1), {}).get(name)
                if ltp is not None:
                    try:
                        indexLtp = float(api.get_quotes(
                            'NSE', ltp)['lp'])
                        self.indexLtpGlobal = indexLtp
                        print(
                            f"{self.req['id']}ltp_from_finvasia...{indexLtp}")

                        if self.req["type"] == "Finvasia":
                            self.finBot.finvasia_indexLtp(
                                api, atm, name, accounts_romil=accounts_romil[0], indexLtp=self.indexLtpGlobal)

                    except Exception as e:
                        print(e)
                        print(
                            f"error in data fatching in finvasia{self.req['id']}")

                symbol = for_ltp.get(tuple(watchlist2), {}).get(name)

                if symbol is not None:
                    try:
                        instruments = pd.DataFrame.from_records(data)
                        indexLtp = obj.ltpData(
                            'NSE', symbol, instruments[instruments.symbol == symbol].iloc[0]['token'])['data']['ltp']
                        self.indexLtpGlobal = indexLtp
                        print(f"ltp_from_angle_one...{indexLtp}")

                        if self.req["type"] == "Angel One":
                            self.angelBot.angel_indexLtp(
                                self.angel_account, atm, symbol=name, accounts_romil=accounts_romil[0], token_df=token_df, indexLtp=self.indexLtpGlobal)

                    except Exception as e:
                        print("error in data fatching in angle one")

            time.sleep(0.5)
