from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.tags import BROKER
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login 

from brokers.helper.angelone.copy_trade import AngelBot
from user.models import DnAngelUserCredsMaster
import json
import logging

class PlaceOrderByAngelMaster(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        user = req["user"]

        broker_creds_objects = DnAngelUserCredsMaster.objects.filter(
            status=1, user=user)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "app_key",
                "totp_key",
                "twoFA",
                userid=F('user_id'),
            ),
        )

        accounts = [
            {
                "userid": str(acc['userid']),
                "app_key": str(acc['app_key']),
                "Qty": str(acc['quantity']),
                "password": str(acc["totp_key"]),
                "twoFA": str(acc["twoFA"]),
            }
            for acc in broker_creds_objects_list
        ]

        try:
            bot = AngelBot(
                master_account=accounts[0],
                other_accounts=accounts[1:],
                logger=logging.getLogger('place_order_by_master_task'),
                user=user
            )

            bot.process_orders()

        except Exception as e:
            print(f'Error :: {e}')
            return

        return Response(data={'message': 'Success'})

