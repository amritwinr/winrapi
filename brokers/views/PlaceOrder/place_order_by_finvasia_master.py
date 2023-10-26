from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.tags import BROKER
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login 

from brokers.tasks import place_order_by_Finvasia_master_task
from user.models import DnFinvasiaUserCredsMaster
import json


class PlaceOrderByFinvasiaMaster(PostLoginAPIView):

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        user = req["user"]

        broker_creds_objects = DnFinvasiaUserCredsMaster.objects.filter(
            status=1, user=user)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "quantity",
                "app_key",
                "twoFA",
                "totp_key",
                "vc",
                "imei",
                "access_token",
                userid=F('user_id'),
            ),
        )

        Response(data={'message': 'Started background task'})

        place_order_by_Finvasia_master_task(
            broker_creds_objects_list, master_id=broker_creds_objects.first().id, user=user)

        return Response(data={'message': 'Started background task'})

