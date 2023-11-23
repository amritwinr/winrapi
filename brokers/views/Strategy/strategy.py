from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView
from user.models import DnRomilBroker, DnAngelUserCredsMaster, DnFinvasiaUserCredsMaster
from django.db.models import F
from brokers.helper.strategy.romil import RomilBot
import logging
import json

class Strategy(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        broker_creds_objects_angel = DnAngelUserCredsMaster.objects.filter(
            user=req["user"])

        broker_creds_objects_finvasuia = DnFinvasiaUserCredsMaster.objects.filter(
            user=req["user"])

        broker_creds_objects_list_angel = list(
            broker_creds_objects_angel.values(
                "api_key",
                "otpToken",
                "password",
                userid=F('user_id'),
            ),
        )

        broker_creds_objects_list_finvasia = list(
            broker_creds_objects_finvasuia.values(
                "password",
                "otpToken",
                "vc",
                "app_key",
                "imei",
                "access_token",
                userid=F('user_id'),
            ),
        )

        accounts_angel = [
            {
                "userid": str(acc['userid']),
                "api_key": str(acc['api_key']),
                "password": str(acc["password"]),
                "twoFA": str(acc["otpToken"]),
            }
            for acc in broker_creds_objects_list_angel
        ]

        accounts_finvasia = [
            {
                "userid": str(acc['userid']),
                "app_key": str(acc['app_key']),
                "password": str(acc["password"]),
                "twoFA": str(acc["otpToken"]),
                "vc": str(acc["vc"]),
                "imei": str(acc["imei"]),
                "access_token": str(acc["access_token"]),
            }
            for acc in broker_creds_objects_list_finvasia
        ]

        broker_creds_objects = DnRomilBroker.objects.filter(user=req["user"])

        broker_creds_objects_list = list(
            broker_creds_objects.values(
                "id",
                "upper_level",
                "lower_level",
                "upper_target",
                "lower_target",
                "sl_upper",
                "sl_lower",
                "strike_ce",
                "strike_pe",
                "quantity",
                "expiry",
                "type",
                "symbol"
            ),
        )

        accounts_romil = [
            {
                "id": str(acc['id']),
                "upper_level": str(acc['upper_level']),
                "lower_level": str(acc['lower_level']),
                "upper_target": str(acc['upper_target']),
                "lower_target": str(acc["lower_target"]),
                "sl_upper": str(acc["sl_upper"]),
                "sl_lower": str(acc["sl_lower"]),
                "strike_ce": str(acc["strike_ce"]),
                "strike_pe": str(acc["strike_pe"]),
                "quantity": str(acc["quantity"]),
                "expiry": str(acc["expiry"]),
                "type": str(acc["type"]),
                "symbol": str(acc["symbol"]),
            }
            for acc in broker_creds_objects_list
        ]

        try:
            bot = RomilBot(
                angel_account= accounts_angel[0] if accounts_angel else [],
                finvasia_account=accounts_finvasia[0] if accounts_finvasia else [],
                other_accounts=accounts_romil,
                logger=logging.getLogger('place_order_by_master_task'),
                req=req
            )

            bot.process_orders()
        except Exception as e:
            print(e)

        return Response()
