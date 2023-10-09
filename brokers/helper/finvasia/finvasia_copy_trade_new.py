# from NorenRestApiPy.NorenApi import NorenApi
from api_helper import ShoonyaApiPy
import pandas as pd
import threading
import logging
import pyotp
import time
import pdb


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
	# {"user": "FA103157", "pwd": "AMri@123", "twoFA": factor2, "vc": "FA103157_U", "app_key": "fba92d1c99c02dc680219f0fa3d10d6e", "imei": "xyz12345","Qty":1},
	# add more account details here
]

ans = {}
for dict in accounts:
		api1 = ShoonyaApiPy()
		ans[user] = api1.login(userid=dict["user"], password=dict["pwd"], twoFA=dict["twoFA"], vendor_code=dict["vc"], api_secret=dict["app_key"], imei=dict["imei"])

 
a = api.get_order_book()
ob = pd.DataFrame(a)
num_rows1 = ob.shape[0]

while True:

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

	print(f"Number 1: {num_rows}, Number 2: {num_rows1}")

	if (num_rows > num_rows):
		print("buy")
	

	# pdb.set_trace()

		def place_order(account):
			ans[user]
			order = api1.place_order(buy_or_sell=trantype, product_type=prdt_type,
									exchange=exch, tradingsymbol=symbol, 
									quantity=Qty*account["Qty"], discloseqty=0,price_type='MKT', price=0, trigger_price=None,
									retention=retention, remarks='my_order_001')
			# print(order)
			print("The order id for account {} is: {}".format(account["user"], order))

		# create a list to hold the threads
		threads = []

		# loop through the accounts and start a thread for each account to place order
		for account in accounts:
			t = threading.Thread(target=place_order, args=(account,))
			t.start()
			threads.append(t)

		# wait for all the threads to complete
		for t in threads:
			t.join()

		print("All orders placed successfully.")
		# pdb.set_trace()
	num_rows1 = ob.shape[0]
	time.sleep(0.5)