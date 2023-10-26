from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.tags import BROKER
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login 

from brokers.helper.FivePaisa.copy_trade import FivePaisaBot
from user.models import Dn5paisaUserCredsMaster
import json
import logging


class PlaceOrderBy5paisaMaster(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        user = req["user"]

        broker_creds_objects = Dn5paisaUserCredsMaster.objects.filter(
            status=1, user=user)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "app_name",
                "app_source",
                "password",
                "user_key",
                "encryption_key",
                "email",
                "passwd",
                "dob",
                "quantity",
                userid=F('user_id'),
            ),
        )

        accounts = [
            {
                "userid": str(acc['userid']),
                "app_name": str(acc['app_name']),
                "app_source": str(acc['app_source']),
                "password": str(acc['password']),
                "user_key": str(acc['user_key']),
                "encryption_key": str(acc['encryption_key']),
                "email": str(acc['email']),
                "passwd": str(acc['passwd']),
                "dob": str(acc['dob']),
                "Qty": str(acc['quantity']),
            }
            for acc in broker_creds_objects_list
        ]

        try:
            bot = FivePaisaBot(
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
