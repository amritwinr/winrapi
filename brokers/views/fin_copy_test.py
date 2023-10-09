from .NorenApi import NorenApi
from .api_helper import ShoonyaApiPy
import pandas as pd
import threading
import logging
import pyotp
import time
import pdb

from brokers.tags import BROKER
from custom_lib.helper import post_login
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.response import Response


class CheckCred(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )

    def post(self, request, *args, **kwargs):

        #start of our program
        api = ShoonyaApiPy()
        token = 'N47YLJ5O5PTKG6L4ZDGI463ZJISEA323' 

        #credentials
        user    = 'FA149805' 
        pwd     = 'Romil@321' 
        factor2 = pyotp.TOTP(token).now()
        
        # print(factor2)
        
        # pdb.set_trace()
        vc      = 'FA149805_U' #USERNAME+_U
        app_key = 'c21400fa59f81eaef9015fb6db7bdd54'
        imei    = 'xyz12345'
        # print(factor2)

        #make the api call
        ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
        # print(ret)

        #first_account
        token1 = 'WFUAJ553LE3QO2E45D4234U6AD4RBJ54'
        factor1 = pyotp.TOTP(token1).now()

        token2 = 'ODZ3332R45EZ22G4F4GZV73X7F7546FS'
        factor2 = pyotp.TOTP(token2).now()
        # print(factor2)

        # pdb.set_trace()

        accounts = [
            {"user": "FA57167", "pwd": "Kiiaan0007@#", "twoFA": factor1, "vc": "FA57167_U", "app_key": "d0e9e7eaccdf08388502bcbda4eee3c6", "imei": "xyz12345","Qty":1},
            {"user": "FA103157", "pwd": "AMri@123", "twoFA": factor2, "vc": "FA103157_U", "app_key": "fba92d1c99c02dc680219f0fa3d10d6e", "imei": "xyz12345","Qty":1},
            # add more account details here
        ]

        # api1 = ShoonyaApiPy()  # Create the master API object outside the loop
        api_objects = {}  # Dictionary to store API objects for each account
        ans = {}  # Dictionary to store responses

        for account in accounts:
            user = account["user"]
            api_objects[user] = ShoonyaApiPy()  # Create an API object for each account
            ans[user] = api_objects[user].login(userid=user, password=account["pwd"], twoFA=account["twoFA"], vendor_code=account["vc"], api_secret=account["app_key"], imei=account["imei"])

        # print(ans)
        # a = api.get_order_book()
        # ob = pd.DataFrame(a)
        # num_rows1 = ob.shape[0]
        # print(a)

        def place_order(api_obj, trantype, prdt_type, exch, symbol, Qty, retention):
            order = api_obj.place_order(buy_or_sell=trantype, product_type=prdt_type,
                                        exchange=exch, tradingsymbol=symbol,
                                        quantity=Qty, discloseqty=0, price_type='MKT', price=0,
                                        trigger_price=None,
                                        retention=retention, remarks='my_order_001')
            print("The order id for account {} is: {}".format(user, order))
            return order

        # while num_rows1:
        a = api.get_order_book()
        ob = pd.DataFrame(a)
        symbol = ob['tsym'].iloc[0]
        trantype = ob['trantype'].iloc[0]
        exch = ob['exch'].iloc[0]
        prdt_type = ob['prd'].iloc[0]
        Qty = ob['qty'].iloc[0]
        price_type = ob['prctyp'].iloc[0]
        retention = ob['ret'].iloc[0]
        status = ob['status'].iloc[0]
        num_rows = ob.shape[0]
        print(num_rows)

        print("Number of orders placed_in master_account:", num_rows)

        # if num_rows > num_rows1:
        print("buy")

        # threads = []

        # for account in accounts:
        #     api_obj = api_objects[account["user"]]
        #     t = threading.Thread(target=place_order, args=(api_obj, trantype, prdt_type, exch, symbol, Qty * account["Qty"], retention))
        #     t.start()
        #     threads.append(t)

        # for t in threads:
        #     t.join()

        print("All orders placed successfully.")
        # num_rows1 = ob.shape[0]
        return Response(status=200)