from SmartApi import SmartConnect

import time
import datetime

import pandas as pd
import pytz
import pyotp
import threading
from user.models import DnAngelUserCredsMaster
from django.db.models import F

import pyotp
import pandas as pd


class AngelBot:

    def __init__(self, master_account, other_accounts, logger, user, max_threads=50):
        self.m_acc = master_account
        self.logger = logger
        self.master_account = master_account
        self.accounts = other_accounts
        self.max_threads = max_threads
        self.user = user

    def place_orderAngel(self):

        broker_creds_objects = DnAngelUserCredsMaster.objects.filter(status=1, user=self.user)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "api_key",
                "password",
                "otpToken",
                userid=F('user_id'),
            ),
        )

        accounts = [
            {
                "userid": str(acc['user_id']),
                "api_key": str(acc['api_key']),
                "Qty": str(acc['quantity']),
                "password": str(acc["password"]),
                "otpToken": str(acc["otpToken"]),
            }
            for acc in broker_creds_objects_list
        ]

        def placeOrderAngel(account):
            # create an object of SmartConnect for the account
            obj = SmartConnect(api_key=account["api_key"])
            factor2 = pyotp.TOTP(account["otpToken"]).now()
            # login to the account
            data = obj.generateSession(
                account["userid"], account["password"], factor2)
            refreshToken = data['data']['refreshToken']

            # fetch the feedtoken for the account
            feedToken = obj.getfeedToken()

            # fetch User Profile for the account
            userProfile = obj.getProfile(refreshToken)

            # place order in the account
            order_params = {
                "variety": self.variety,
                "tradingsymbol": self.tradingsymbol,
                "symboltoken": self.symboltoken,
                "transactiontype": self.transactiontype,
                "exchange": self.exchange,
                "ordertype": self.ordertype,
                "producttype": self.producttype,
                "duration": self.duration,
                "price": "0",
                "squareoff": "0",
                "stoploss": "0",
                "quantity": int(account["Qty"]) * int(self.quantity),
            }
            order_id = obj.placeOrder(order_params)
            print("The order id for account {} is: {}".format(
                account["userid"], order_id))

        threads = []

        # loop through the accounts and start a thread for each account to place order
        for account in accounts[1:]:
            t = threading.Thread(target=placeOrderAngel, args=(account,))
            t.start()
            threads.append(t)

    def process_orders(self):

        ist = pytz.timezone('Asia/Kolkata')
        target_time = ist.localize(
            datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                              23, 59))

        obj = SmartConnect(api_key=self.master_account["api_key"])
        factor1 = pyotp.TOTP(self.master_account["otpToken"]).now()

        # login api call
        data = obj.generateSession(
            self.master_account["userid"], self.master_account["password"], factor1)
        refreshToken = data['data']['refreshToken']

        # fetch the feedtoken
        feedToken = obj.getfeedToken()

        # fetch User Profile
        userProfile = obj.getProfile(refreshToken)
        # print(userProfile)

        order = obj.orderBook()
        # ['tradingsymbol'],['variety']#.iloc[0]variety
        df = pd.DataFrame(order['data'])
        num_rows1 = df.shape[0]

        while True:
            broker_creds_objects = DnAngelUserCredsMaster.objects.filter(user=self.user)

            broker_creds_objects_list = list(
                broker_creds_objects.values(
                    "status",
                ),
            )

            accounts = [
                {
                    "status": str(acc["status"]),
                }
                for acc in broker_creds_objects_list
            ]

            if accounts[0]['status'] == '0':
                break

            current_time = datetime.datetime.now(ist)

            if current_time > target_time:
                print("Current time is greater than 3:30 PM IST. Stopping the loop.")
                self.logger.info(
                    "Current time is greater than 3:30 PM IST. Stopping the loop.")
                break

            order = obj.orderBook()
            # ['tradingsymbol'],['variety']#.iloc[0]variety
            df = pd.DataFrame(order['data'])

            self.map_order_detailsAngel(ob=df)
            num_rows = df.shape[0]

            print({"num rows": num_rows, "num_rows1": num_rows1})

            if num_rows1 > 0:
                if num_rows > num_rows1:
                    self.place_orderAngel()

            num_rows1 = df.shape[0]
            time.sleep(0.5)

    def map_order_detailsAngel(self, ob):
        try:
            self.variety = ob['variety'].iloc[-1]
            self.tradingsymbol = ob['tradingsymbol'].iloc[-1]
            self.symboltoken = ob['symboltoken'].iloc[-1]
            self.transactiontype = ob['transactiontype'].iloc[-1]
            self.exchange = ob['exchange'].iloc[-1]
            self.ordertype = ob['ordertype'].iloc[-1]
            self.producttype = ob['producttype'].iloc[-1]
            self.duration = ob['duration'].iloc[-1]
            self.price = ob['price'].iloc[-1]
            self.squareoff = ob['squareoff'].iloc[-1]
            self.stoploss = ob['stoploss'].iloc[-1]
            self.quantity = ob['quantity'].iloc[-1]
        except Exception as e:
            print(e)
