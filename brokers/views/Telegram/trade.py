from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.tags import BROKER
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login 

from brokers.helper.Telegram.copy_trade import TelegramBot
from user.models import DnTelegramSubscribe, DnTelegram, DnFinvasiaUserCredsMaster
import json
import logging


class PlaceOrderByTelegram(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        user = req["user"]

        print({"user": user})

        broker_creds_objects = DnTelegram.objects.filter(user=user)

        broker_creds_objects_broker = DnFinvasiaUserCredsMaster.objects.filter(user=user)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        if broker_creds_objects_broker.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "api_hash",
                "api_id",
                "phone",
            ),
        )

        broker_creds_objects_list_broker = list(
            broker_creds_objects_broker.values(
                "user_id",
                "password",
                "access_token",
            ),
        )

        account = [
            {
                "api_hash": str(acc['api_hash']),
                "api_id": str(acc['api_id']),
                "phone": str(acc['phone']),
            }
            for acc in broker_creds_objects_list
        ]

        account_finvasia = [
            {
                "userid": str(acc['user_id']),
                "password": str(acc['password']),
                "access_token": str(acc['access_token']),
            }
            for acc in broker_creds_objects_list_broker
        ]

        try:
            bot = TelegramBot(
                account=account[0],
                req=req,
                finvasia_account=account_finvasia[0]
            )

            bot.trade()

        except Exception as e:
            print(f'Error :: {e}')
            return Response(data={'message': 'Success'})

        return Response(data={'message': 'Success'})
