from py5paisa import FivePaisaClient
from py5paisa.order import Order, OrderType, Exchange
import time
import datetime

import pandas as pd
import pytz
import pyotp
import threading
from user.models import Dn5paisaUserCredsMaster
from django.db.models import F
import pyotp
import pandas as pd
import threading
import json


class FivePaisaBot:

    def __init__(self, master_account, other_accounts, logger, user, max_threads=50):
        self.m_acc = master_account
        self.logger = logger
        self.master_account = master_account
        self.accounts = other_accounts
        self.max_threads = max_threads
        self.user = user

    def place_order(self):

        broker_creds_objects = Dn5paisaUserCredsMaster.objects.filter(status=1, user=self.user)
        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "app_name",
                "app_source",
                "password",
                "user_key",
                "encryption_key",
                "email",
                "passwd",
                "dob",
                "quantity",
                userid=F('user_id'),
            ),
        )

        acc_cred = [{
            "APP_NAME": str(acc['app_name']),
            "APP_SOURCE": str(acc['app_source']),
            "PASSWORD": str(acc['password']),
            "USER_KEY": str(acc['user_key']),
            "ENCRYPTION_KEY": str(acc['encryption_key']),
            "UBfFkcEbF5C": str(acc['userid']),
        }
            for acc in broker_creds_objects_list
        ][1:]

        accounts = [
            {
                "email": str(acc['email']),
                "passwd": str(acc['passwd']),
                "dob": str(acc['dob']),
                "Qty": str(acc['quantity']),
            }
            for acc in broker_creds_objects_list
        ][1:]

        def place_order_for_account(cred, account):
            client = FivePaisaClient(email=account['email'], passwd=account['passwd'], dob=account['dob'],cred=cred)
            client.login()

            try:
                order = client.place_order(OrderType=self.BuySell,Exchange='N',ExchangeType=self.ExchType, ScripCode=self.ScripCode, Qty=self.Qty, Price=0)
                print("The order id for account {} is: {}".format(account["email"], order))

                return order
            except Exception as e:
                self.logger.error(
                    f"Error placing order for account {account['user_id']}: {e}")

        threads = []

        for i in range(2):

            t = threading.Thread(
                target=place_order_for_account, args=(acc_cred[i], accounts[i]))
            t.start()
            threads.append(t)
            self.logger.info("All orders placed successfully.")

        for t in threads:
            t.join()

        # api_objects[user].logout()

    def process_orders(self):
        cred = {
            "APP_NAME": self.master_account["app_name"],
            "APP_SOURCE": self.master_account["app_source"],
            "USER_ID": self.master_account["userid"],
            "PASSWORD": self.master_account["password"],
            "USER_KEY": self.master_account["user_key"],
            "ENCRYPTION_KEY": self.master_account["encryption_key"],
        }

        client = FivePaisaClient(
            email=self.master_account["email"], passwd=self.master_account["passwd"], dob=self.master_account["dob"], cred=cred)
        client.login()

        order = client.get_tradebook()
        df = pd.DataFrame(order)
        num_rows1 = df.shape[0]

        ist = pytz.timezone('Asia/Kolkata')
        target_time = ist.localize(
            datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                              23, 59))

        while True:
            broker_creds_objects = Dn5paisaUserCredsMaster.objects.filter(user=self.user)

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

            order = client.get_tradebook()
            df = pd.DataFrame(order)
            ob = df['TradeBookDetail']

            df = json.dumps(df['TradeBookDetail'].iloc[-1])
            df = df.replace("'", '"')
            df = json.loads(df)

            self.map_order_details(ob=df)
            num_rows = ob.shape[0]

            self.logger.info(
                f"Number 1: {num_rows}, Number 2: {num_rows1}")

            if num_rows1 > 0:
                if num_rows > num_rows1:
                    self.place_order()

            num_rows1 = df.shape[0]
            time.sleep(0.5)

    def map_order_details(self, ob):
        try:
            self.BuySell = ob['BuySell']
            self.trantype = ob['Exch']
            self.ExchType = ob['ExchType']
            self.ScripCode = ob['ScripCode']
            self.Qty = ob['Qty']
        except Exception as e:
            print(e)
