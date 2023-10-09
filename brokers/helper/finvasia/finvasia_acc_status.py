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
print(ret["actid"])