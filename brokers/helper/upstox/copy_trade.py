import upstox_client
from upstox_client.rest import ApiException

import time
import datetime

import pandas as pd
import pytz
import pyotp
import threading
from user.models import DnUpstoxUserCredsMaster
from django.db.models import F

import pyotp
import pandas as pd


class UpstoxBot:

    def __init__(self, master_account, other_accounts, logger, user, max_threads=50):
        self.m_acc = master_account
        self.logger = logger
        self.master_account = master_account
        self.accounts = other_accounts
        self.max_threads = max_threads
        self.user = user

    def place_order(self):

        broker_creds_objects = DnUpstoxUserCredsMaster.objects.filter(
            status=1, user=self.user)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "access_token",
                userid=F('user_id'),
            ),
        )

        accounts = [
            {
                "userid": str(acc['userid']),
                "Qty": str(acc['quantity']),
                "access_token": str(acc["access_token"]),
            }
            for acc in broker_creds_objects_list
        ]

        def placeOrder(account):
            try:
                configuration = upstox_client.Configuration()
                configuration.access_token = account["access_token"]
                api_instance = upstox_client.OrderApi(
                    upstox_client.ApiClient(configuration))
                api_version = '2.0'

                body = upstox_client.PlaceOrderRequest(quantity=int(account["Qty"]) * int(self.quantity[0]),
                                                       product=self.product[0],
                                                       validity=self.validity[0],
                                                       price=0,
                                                       instrument_token=self.instrument_token[0],
                                                       order_type=self.order_type[0],
                                                       transaction_type=self.transaction_type[0],
                                                       disclosed_quantity=0,
                                                       trigger_price=0,
                                                       is_amo=False)
                api_response = api_instance.place_order(body, api_version)
                print("The order id for account {} is: {}".format(
                    account["userid"], api_response))
                return api_response

            except Exception as e:
                self.logger.error(
                    f"Error placing order for account {account['userid']}: {e}")

        threads = []

        # loop through the accounts and start a thread for each account to place order
        for account in accounts[1:]:
            t = threading.Thread(target=placeOrder, args=(account,))
            t.start()
            threads.append(t)
            self.logger.info("All orders placed successfully.")

        for t in threads:
            t.join()

    def process_orders(self):
        ist = pytz.timezone('Asia/Kolkata')
        target_time = ist.localize(
            datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                              23, 59))

        configuration = upstox_client.Configuration()
        configuration.access_token = self.master_account["access_token"]

        api_instance = upstox_client.OrderApi(
            upstox_client.ApiClient(configuration))

        api_version = '2.0'  # str | API Version Header
        api_response = api_instance.get_order_book(api_version)

        data = api_response._data
        df = pd.DataFrame(data)
        num_rows1 = df.shape[0]

        while True:
            broker_creds_objects = DnUpstoxUserCredsMaster.objects.filter(
                user=self.user)

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

            api_response = api_instance.get_order_book(api_version)
            data = api_response._data
            df = pd.DataFrame(data)
            self.map_order_detailsAngel(df)
            num_rows = df.shape[0]

            # print(self.product)

            print({"num rows": num_rows, "num_rows1": num_rows1})

            if num_rows1 > 0:
                if num_rows > num_rows1:
                    self.place_order()

            num_rows1 = df.shape[0]
            time.sleep(0.5)

    def map_order_detailsAngel(self, df):
        try:
            self.quantity = df[0].iloc[0]._quantity,
            self.product = df[0].iloc[0]._product,
            self.validity = df[0].iloc[0]._validity,
            self.instrument_token = df[0].iloc[0]._instrument_token,
            self.order_type = df[0].iloc[0]._order_type,
            self.transaction_type = df[0].iloc[0]._transaction_type,
        except Exception as e:
            print({"e": e})
