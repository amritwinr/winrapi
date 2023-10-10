from .api_helper import ShoonyaApiPy
import time
import datetime

import pandas as pd
import pytz
import pyotp
import threading
from user.models import DnFinvasiaUserCredsMaster
from django.db.models import F

class FinvaciaBot:

    def __init__(self, master_account, other_accounts, logger, max_threads=50):
        self.m_acc = master_account
        self.logger = logger
        self.master_account = master_account
        self.accounts = other_accounts
        self.max_threads = max_threads

    def get_order_book(self):

        api = ShoonyaApiPy()

        account = self.m_acc
        factor2 = pyotp.TOTP(account['twoFA']).now()

        api.login(
            userid=account["userid"],
            twoFA=factor2,
            password=account["password"],
            vendor_code=account["vc"],
            api_secret=account["app_key"],
            imei=account["imei"],
        )

        while True:
            try:
                order_history = api.get_order_book()
                result = pd.DataFrame(order_history)

                return result, result.shape[0]
            except Exception as e:
                self.logger.error(f"Error fetching order history data: {e}")

    def place_order(self):
        broker_creds_objects = DnFinvasiaUserCredsMaster.objects.filter(status=1)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "app_key",
                "twoFA",
                "totp_encrypt_key",
                "vc",
                "imei",
                userid=F('broker_user_id'),
            ),
        )

        accounts = [
            {
            "userid": str(acc['userid']),
            "app_key": str(acc['app_key']),
            "Qty": str(acc['quantity']),
            "twoFA": str(acc["twoFA"]),
            "password": str(acc["totp_encrypt_key"]),
            "vc": str(acc["vc"]),
            "imei": str(acc["imei"]),
            }
            for acc in broker_creds_objects_list
        ]


        api_objects = {}
        ans = {}

        for account in accounts[1:]:
            factor = pyotp.TOTP(account['twoFA']).now()
            user = account["userid"]
            api_objects[user] = ShoonyaApiPy()  # Create an API object for each account
            ans[user] = api_objects[user].login(userid=account["userid"], password=account["password"], twoFA=factor, vendor_code=account["vc"], api_secret=account["app_key"], imei=account["imei"])

        def place_order_for_account(api_obj, account):
            try:
                order = api_obj.place_order(
                    buy_or_sell=self.trantype,
                    product_type=self.prdt_type,
                    exchange=self.exch,
                    tradingsymbol=self.symbol,
                    quantity=int(account["Qty"]) * int(self.Qty),
                    discloseqty=0,
                    price_type=self.price_type,
                    price=0,
                    trigger_price=None,
                    retention=self.retention,
                    remarks='my_order_001'
                )
                print(f"The order id for account {account['userid']} is: {order}")
                return order
            except Exception as e:
                self.logger.error(
                    f"Error placing order for account {account['userid']}: {e}")

        threads = []
                   
        for account in accounts[1:]:
            api_obj = api_objects[account["userid"]]
            t = threading.Thread(target=place_order_for_account, args=(api_obj, account))
            t.start()
            threads.append(t)
            self.logger.info("All orders placed successfully.")

        for t in threads:
            t.join()

        # api_objects[user].logout()
            
    def process_orders(self):
        api = ShoonyaApiPy()
        factor2 = pyotp.TOTP(self.master_account['twoFA']).now()

        api.login(
            userid=self.master_account["userid"],
            twoFA=factor2,
            password=self.master_account["password"],
            vendor_code=self.master_account["vc"],
            api_secret=self.master_account["app_key"],
            imei=self.master_account["imei"],
        )

        order_history = api.get_order_book()
        result = pd.DataFrame(order_history)
        num_rows1 = result.shape[0]

        ist = pytz.timezone('Asia/Kolkata')
        target_time = ist.localize(
            datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                              23, 59))

        while True:      
            broker_creds_objects = DnFinvasiaUserCredsMaster.objects.filter()

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

            order_book = api.get_order_book()
            ob = pd.DataFrame(order_book)
            self.map_order_details(ob)
            num_rows = ob.shape[0]

            self.logger.info(
                f"Number 1: {num_rows}, Number 2: {num_rows1}")

            if num_rows1 > 0:
                if num_rows > num_rows1:
                    self.place_order()
                        
            num_rows1 = ob.shape[0]
            time.sleep(0.5)

    def map_order_details(self, ob):
        try:
            self.symbol = ob['tsym'].iloc[0]
            self.trantype = ob['trantype'].iloc[0]
            self.exch = ob['exch'].iloc[0]
            self.prdt_type = ob['prd'].iloc[0]
            self.Qty = ob['qty'].iloc[0]
            self.price_type = ob['prctyp'].iloc[0]
            self.retention = ob['ret'].iloc[0]
            self.status = ob['status'].iloc[0]
        except Exception as e:
            print(e)




# master_account = {
#     "userid": 'FA149805',
#     "twoFA": "N47YLJ5O5PTKG6L4ZDGI463ZJISEA323",
#     "password": 'Romil@321',
#     "vc": 'FA149805_U',
#     "app_key": "c21400fa59f81eaef9015fb6db7bdd54",
#     "imei": "xyz12345"
# }


# other_accounts = {
#     "userid": "FA57167",
#     "twoFA": "WFUAJ553LE3QO2E45D4234U6AD4RBJ54",
#     "password": "Kiiaan0007@#",
#     "vc": "FA57167_U",
#     "app_key": "d0e9e7eaccdf08388502bcbda4eee3c6",
#     "imei": "xyz12345",
#     "Qty": 1
# },

# k = FinvaciaBot(master_account=master_account,
#                 other_accounts=other_accounts, logger=logging)
# s = k.place_order_for_account()

# print(s)
