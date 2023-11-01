from typing import Any
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView
import json
from user.models import DnTelegram
from telethon.sync import TelegramClient
import asyncio
import time
from asgiref.sync import sync_to_async
from telethon import errors
import os
from threading import Thread

class Telegram(PostLoginAPIView):

    def __init__(self,):
        Thread.__init__(self)
        self.client = 0
        self.phone_code_hash = ""
        self.req = {}
        self.usernames = []
        print({"path" : os.path.abspath("./")})

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login
    )
    def post(self, request, *args, **kwargs):
        self.req = json.loads(request.body.decode("utf-8"))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.client = TelegramClient(
            os.path.abspath("./"+self.req["phone"]), int(self.req["apiId"]), self.req["apiHash"], loop=loop)

        async def handle(loop):

            try:
                await self.client.connect()

                if not await self.client.is_user_authorized():
                    phone_code = await self.client.send_code_request(phone=self.req["phone"])
                    self.phone_code_hash = phone_code.phone_code_hash

                while True:
                    print("loop started") 

                    @sync_to_async 
                    def db():
                        data = DnTelegram.objects.filter(user=self.req["user"])
                        dataList = list(
                            data.values(
                                "code", 
                            ),
                        )
                        return dataList

                    dataList = await db()

                    print({"data": dataList})

                    if len(dataList) > 0:
                        code = dataList[0]['code']

                        try:
                            if not await self.client.is_user_authorized():
                                await self.client.sign_in(phone=self.req["phone"], code=code, phone_code_hash=self.phone_code_hash)

                                @sync_to_async
                                def db():
                                    data = DnTelegram.objects.get(
                                        user=self.req["user"])
                                    data.api_id = self.req["apiId"]
                                    data.api_hash = self.req["apiHash"]
                                    data.phone = self.req["phone"]
                                    data.isAuthorized = True
                                    data.save()

                                await db()

                            dialogs = await self.client.get_dialogs()

                            for dialog in dialogs:
                                if hasattr(dialog.entity, 'username') and dialog.entity.username:
                                    self.usernames.append(
                                        dialog.entity.username)

                        except Exception as e:
                            print(f"Error: {e}")

                        await self.client.disconnect()

                        break
                    time.sleep(1)

            except errors.FloodWaitError as e:
                print('Flood wait for ', e.seconds)
                exit

        self.client.loop.run_until_complete(handle(loop=self.client.loop))

        return Response(data=self.usernames)
