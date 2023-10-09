from pya3 import *
import pdb
import time


# user_id = '611899'
# api_key = 'LY4n3H0Db1F3hS4Zsx1VjRn3ra2Wj7iYpSqLgWD4d7uuNSAF9u4rD8bmmCpPsFORLrdDormNKzVuyu64b2bGitoPGJ1V6HWKPtbM9lTC0lvmdUigbMv2d6F9qyl8J1hn'


user_id = '929402'
api_key = '2St0KTyJxcAnOb51haiQSpEQvnhx1jobnuBOvunmedT0i9rHkZjlnrS6el7Lyi1aDeW1gVvyokWv61VLq9kMjK981X2iXJB2fsrsCMWFBmrAf1tjxbqflDQSYtGELyFx'
 
alice = Aliceblue(user_id=user_id, api_key=api_key)
print(alice.get_session_id())


# pdb.set_trace()

accounts = [
	{"userid":"473680", "api_key":"U8rxQLKMOzrMkcaktDElMcNRYbZJq4iIQUkTZo1FnyjTgGvKimKUMlILfecEUyFUR4HJ6rFQVnznucia0X00sxCkErQ0sIr8XSvXYtKI7oghf0qiff70q0MoBibP7DR3"},
]

a = alice.get_order_history('')
if 'emsg' in a and a['emsg'] == 'No Data':
	print("you have no placed order till now ")
	# ob = pd.DataFrame(a)
else:
	ob = pd.DataFrame(a)
	num_rows1 = ob.shape[0]

     
while True:

	ob = alice.get_order_history('')[0]
	t_type = ob['Trantype']
	t_type_map = {'B': TransactionType.Buy, 'S': TransactionType.Sell}
	t_type = t_type_map.get(t_type, 'Unknown') 
	exch = ob['Exchange']	 
	# symbol = ob['Trsym']
	symbol = ob['Scripname']
	# print(symbol)	 
	Qty = ob['Qty']	 
	o_type = ob['Prctype']
	o_type_map = {'L': OrderType.Limit, 'MKT': OrderType.Market}
	o_type = o_type_map.get(o_type, 'Unknown')	 
	p_type = ob['Pcode']
	p_type_map = {'NRML': ProductType.Delivery, 'MIS': ProductType.Intraday}
	p_type = p_type_map.get(p_type, 'Unknown')	 
	status = ob['Status']
	# print(status)
	 


	a = alice.get_order_history('')
	ob = pd.DataFrame(a)
	num_rows = ob.shape[0]
	print("Number of order placed_in master_account:", num_rows)

	if (num_rows > num_rows1):
		print("buy")


		def place_order(account):

			alice = Aliceblue(user_id=account['userid'], api_key=account['api_key'])
			alice.get_session_id()
			 
			order = alice.place_order(transaction_type = t_type ,
									instrument = alice.get_instrument_by_symbol(exch, symbol), 
									quantity = Qty, 
									order_type = o_type, 
									product_type = p_type)
			# print(order)
			print("The order id for account {} is: {}".format(account["userid"], order))

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
	num_rows1 = ob.shape[0]
	time.sleep(0.5)
 
















# user_id = '922647'
# api_key = 'NijgbSDCbmX5yz5iklSITIJ9P6Zd1GqFzuKSQevDhdaE6gSOPooEuDyAelbnQFREAg8u3Kou89xfWsFSxUb11vO2yFvy9r4egDJPqzLFfZbzGZTW7QSQurKKSTKsWi8m'
