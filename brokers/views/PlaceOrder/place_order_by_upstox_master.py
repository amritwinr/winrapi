from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.tags import BROKER
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login 


from brokers.helper.upstox.copy_trade import UpstoxBot
from user.models import  DnUpstoxUserCredsMaster
import json
import logging

class PlaceOrderByUpstoxMaster(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        user = req["user"]

        broker_creds_objects = DnUpstoxUserCredsMaster.objects.filter(
            status=1, user=user)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "access_token",
                userid=F('api_key'),
            ),
        )

        accounts = [
            {
                "userid": str(acc['userid']),
                "Qty": str(acc['quantity']),
                "access_token": str(acc["access_token"]),
            }
            for acc in broker_creds_objects_list
        ]

        try:
            bot = UpstoxBot(
                master_account=accounts[0],
                other_accounts=accounts[1:],
                logger=logging.getLogger('place_order_by_master_task'),
                user=user,
            )

            bot.process_orders()

        except Exception as e:
            print(f'Error :: {e}')
            return

        return Response(data={'message': 'Success'})

