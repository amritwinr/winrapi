import time
import datetime

import pandas as pd
from concurrent.futures import ThreadPoolExecutor

import pytz
from pya3 import Aliceblue, TransactionType, OrderType, ProductType


class TradingBot:
    def __init__(self, master_account, other_accounts, logger, max_threads=50):
        self.logger = logger
        self.master_account = Aliceblue(user_id=master_account["userid"], api_key=master_account["api_key"])
        self.accounts = other_accounts
        self.order_history_df = pd.DataFrame()
        self.num_rows1 = 0
        self.max_threads = max_threads

        self.logger.info(f"master_account :: {master_account}")
        self.logger.info(f"other_accounts :: {other_accounts}")

        # self.master_account_qty = master_account['Qty']

    def fetch_master_session_id(self):
        return self.master_account.get_session_id()

    def fetch_all_session_ids(self):
        ans = {}
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            results = executor.map(self.fetch_session_for_account, self.accounts)
        for r in results:
            ans.update(r)
        return ans

    def fetch_session_for_account(self, account):
        try:
            alice_instance = Aliceblue(user_id=account["userid"], api_key=account["api_key"])
            return {account["userid"]: alice_instance.get_session_id()}
        except Exception as e:
            self.logger.error(f"Error fetching session for account {account['userid']}: {e}")
            return {}

    def fetch_order_history(self):
        while True:
            try:
                order_history = self.master_account.get_order_history('')
                if 'emsg' in order_history and order_history['emsg'] == 'No Data':
                    self.logger.info("You have no placed order till now.")
                else:
                    # self.order_history_df = pd.DataFrame(order_history)
                    # self.num_rows = self.order_history_df.shape[0]
                    result = pd.DataFrame.from_records(order_history)
                    return result, result.shape[0]
            except Exception as e:
                self.logger.error(f"Error fetching order history data: {e}")

    def place_order_for_account(self, account):
        try:
            alice_instance = Aliceblue(user_id=account["userid"], api_key=account["api_key"])
            alice_instance.get_session_id()
            print(self.exch, self.symbol, '????????????')
            print(alice_instance.get_instrument_by_symbol(self.exch, self.symbol))
            order = alice_instance.place_order(
                transaction_type=self.t_type,
                instrument=alice_instance.get_instrument_by_symbol(self.exch, self.symbol),
                quantity=int(account["Qty"]) * int(self.account_qty),
                order_type=self.o_type,
                product_type=self.p_type
            )
            self.logger.info(f"The order id for account {account['userid']} is: {order}")
        except Exception as e:
            self.logger.error(f"Error placing order for account {account['userid']}: {e}")

    def process_orders(self):
        ist = pytz.timezone('Asia/Kolkata')
        target_time = ist.localize(
            datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
                              22, 00))

        while True:
            current_time = datetime.datetime.now(ist)
            if current_time > target_time:
                self.logger.info("Current time is greater than 3:30 PM IST. Stopping the loop.")
                break

            if self.order_history_df.shape[0] >= 1:
                ob = self.master_account.get_order_history('')
                if len(ob) > 0:
                    ob = ob[0]
                    self.map_order_details(ob)
                    self.order_history_df, num_rows = self.fetch_order_history()
                    self.logger.info(f"Number of orders placed in master account: {num_rows}")

                    if num_rows > self.num_rows1:
                        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                            executor.map(self.place_order_for_account, self.accounts)
                        self.logger.info("All orders placed successfully.")
                    self.num_rows1 = self.order_history_df.shape[0]
            time.sleep(0.5)

    def map_order_details(self, ob):
        self.t_type_map = {'B': TransactionType.Buy, 'S': TransactionType.Sell}
        self.t_type = self.t_type_map.get(ob['Trantype'], 'Unknown')

        self.o_type_map = {'L': OrderType.Limit, 'MKT': OrderType.Market}
        self.o_type = self.o_type_map.get(ob['Prctype'], 'Unknown')

        self.p_type_map = {'NRML': ProductType.Delivery, 'MIS': ProductType.Intraday}
        self.p_type = self.p_type_map.get(ob['Pcode'], 'Unknown')

        self.exch = ob['Exchange']
        self.symbol = ob['Trsym']
        self.account_qty = ob['Qty']
        self.status = ob['Status']
