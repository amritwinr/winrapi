from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from brokers.tags import BROKER
from brokers.tasks import place_order_by_master_task
from custom_lib.api_view_class import PostLoginAPIView
from custom_lib.helper import post_login 


from brokers.helper.upstox.copy_trade import UpstoxBot
from brokers.helper.angelone.copy_trade import AngelBot
from brokers.helper.FivePaisa.copy_trade import FivePaisaBot
from brokers.tasks import place_order_by_Finvasia_master_task
from user.models import DnBrokerUserCredsMaster, DnFinvasiaUserCredsMaster, DnAngelUserCredsMaster, DnUpstoxUserCredsMaster, Dn5paisaUserCredsMaster
import json
import logging

class PlaceOrderByMaster(PostLoginAPIView):

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        broker_id = request.brokerid
        user_id = request.userid

        if broker_id == -1:
            raise Exception(12012)

        broker_creds_objects = DnBrokerUserCredsMaster.objects.filter(
            user_id=user_id, broker_id=broker_id)

        if broker_creds_objects.count() == 0:
            return Response(data={'message': "No broker creds found"}, status=status.HTTP_400_BAD_REQUEST)

        if broker_creds_objects.first().is_background_task_running:
            return Response(data={'message': 'Already running background task'})

        broker_creds_objects_list = list(
            broker_creds_objects.values("quantity", userid=F(
                'broker_user_id'), api_key=F('broker_api_key'))
        )
        place_order_by_master_task.delay(
            broker_creds_objects_list, master_id=broker_creds_objects.first().id)

        master = broker_creds_objects.first()
        master.is_background_task_running = True
        master.save()

        return Response(data={'message': 'Started background task'})


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

        master = broker_creds_objects.first()
        master.is_background_task_running = True
        master.save()

        return Response(data={'message': 'Started background task'})


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
