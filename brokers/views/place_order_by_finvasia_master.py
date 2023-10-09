import logging

from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.helper.aliceblue.copy_trade import TradingBot
from brokers.tags import BROKER
from brokers.tasks import place_order_by_Finvasia_master_task
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login
from user.models import DnFinvasiaUserCredsMaster
import json

class PlaceOrderByMaster(PostLoginAPIView):

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        broker_id = request.brokerid
        user_id = request.userid

        req = json.loads(request.body.decode("utf-8"))


        # if button == 0:
        #     return Response(data={'message': 'Stopped Background Task'})

        if broker_id == -1:
            raise Exception(12012)

        broker_creds_objects = DnFinvasiaUserCredsMaster.objects.filter(
            user_id=user_id, broker_id=broker_id, status=1)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        # if broker_creds_objects.first().is_background_task_running:
        #     return Response(data={'message': 'Already running background task'}
        
        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "app_key",
                "twoFA",
                "totp_encrypt_key",
                "vc",
                "imei",
                userid=F('broker_user_id'),
            ),
        )

        Response(data={'message': 'Started background task'})

        place_order_by_Finvasia_master_task(
            broker_creds_objects_list, master_id=broker_creds_objects.first().id)

        master = broker_creds_objects.first()
        master.is_background_task_running = True
        master.save()

        return Response(data={'message': 'Started background task'})
