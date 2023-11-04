from telethon.sync import TelegramClient
import pandas as pd
import time
from datetime import datetime, timedelta
import pytz
import asyncio
import os
from user.models import DnTelegramSubscribe
from datetime import datetime
import re


class TelegramBot:

    def __init__(self, account, req):
        self.account = account
        self.req = req
        self.removed = []
        self.filePath = './Files/'+account['phone']+'_'+req['name']+".txt"

    def placeorder(self, date, text, tl_data):
        # with open(self.filePath, 'a') as file:
        #     # Write some data to the file
        #     file.writelines(str(date) + "\n")

        tl_msg = str(text)
        tl_msg = tl_msg.upper()

        dicts = {'Nifty': 1, "50": 2}

        listData = tl_data["symbols"].split(',')
        listData = [word.strip() for word in listData]

        result = {}
        for key in listData:
            if key in dicts:
                result[key] = dicts[key]

        symbol = {"tsym": result}
        BUY_SELL = ["BUY", "SELL"]
        CE_PE = ["CE", "PE"]

        name_count = sum(1 for word in tl_msg.split()
                         if word in symbol["tsym"])
        LIST1 = [
            next((symbol["tsym"][word]
                 for word in tl_msg.split() if word in symbol["tsym"]), None)
        ] if name_count == 1 else ["Plz_write_one_name"]

        # #condition for index and stocks_option only
        if "Plz_write_one_name" not in LIST1 and any(word in LIST1 for word in LIST1) and any(word in tl_msg for word in BUY_SELL) and any(word in tl_msg for word in CE_PE):
            number_match = re.search(r'\d+', tl_msg)
            if number_match:
                number = number_match.group(0)
                print(f"first con. meet")
                print(LIST1)
                print([word for word in tl_msg.split() if word in BUY_SELL])
                print([word for word in tl_msg.split() if word in CE_PE])
                print(number)

        if "Plz_write_one_name" not in LIST1 and any(word in LIST1 for word in LIST1) and any(word in tl_msg for word in BUY_SELL) and not any(word in tl_msg for word in CE_PE):
            number_match = re.search(r'\d+', tl_msg)
            if number_match:
                number = number_match.group(0)
                print(f"second con. meet")
                print(LIST1)
                print([word for word in tl_msg.split() if word in BUY_SELL])
                print(number)

        self.removed.append(date)

    def trade(self):
        phone = self.account["phone"]

        symbols = self.req["symbols"]
        quantity = self.req["quantity"]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        chat = self.req["name"]

        with TelegramClient(os.path.abspath(self.account["phone"]), self.account["api_id"], self.account["api_hash"]) as client:

            while True:
                self.df = pd.DataFrame(
                    columns=["group", "sender", "text", "date"])

                broker_creds_objects = DnTelegramSubscribe.objects.filter(
                    id=self.req["id"])

                if broker_creds_objects.count() == 0:
                    # if os.path.exists(self.filePath):
                    #     os.remove(self.filePath)
                    #     print(f"{self.filePath} has been deleted.")
                    # else:
                    #     print(f"{self.filePath} does not exist.")
                    break

                broker_creds_objects_list = list(
                    broker_creds_objects.values(
                        "quantity",
                        "name",
                        "symbols",
                    ),
                )

                tl_data = [
                    {
                        "quantity": str(acc['quantity']),
                        "name": str(acc['name']),
                        "symbols": str(acc['symbols']),
                    }
                    for acc in broker_creds_objects_list
                ]

                print(tl_data)

                for message in client.iter_messages(chat, offset_date=datetime.now() - timedelta(days=1), reverse=True):
                    data = {"group": chat, "sender": message.sender_id,
                            "text": message.text, "date": pd.to_datetime(message.date)}
                    temp_df = pd.DataFrame(data, index=[1])

                    self.df = pd.concat([self.df, temp_df], ignore_index=True)

                    if message.date not in self.removed:
                        self.placeorder(date=message.date,
                                        text=message.text, tl_data=tl_data[0])

                    # if os.path.exists(self.filePath):
                    #     with open(self.filePath, 'r') as file:
                    #         # file_size = os.path.getsize(self.filePath)
                    #         # if file_size == 0:
                    #         #     self.placeorder(text=message.date)
                    #         # else:
                    #         for line in file:
                    #                 d = datetime.strptime(
                    #                     line, "%Y-%m-%d %H:%M:%S%z")

                    #                 if message.date != d:
                    #                     self.placeorder(text=message.date)

                    # else:
                    #     self.placeorder(text=message.date)

                    # print(self.df['date'].isin([temp_df.iloc(1)[3].tolist()[0]]))
                    self.df['date'] = self.df['date'].apply(
                        lambda x: x.astimezone(pytz.timezone('Asia/Kolkata')))
                # s = self.df['date'].isin([lists[-1].iloc(0)[0]["date"]]).iloc(0)[-1]

                time.sleep(0.25)
