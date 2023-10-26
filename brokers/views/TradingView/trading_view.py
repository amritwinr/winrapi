from rest_framework.response import Response
from user.models import DnFinvasiaUserCredsMaster
from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import AllowAny
from brokers.helper.tradingview.finvasia_trading_view import FinvaciaTradingBot


class FinvasiaTradingView(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        req = request.GET.dict()

        broker_creds_objects_finvasuia = DnFinvasiaUserCredsMaster.objects.filter(
            unique_code=req["unique_code"])

        broker_creds_objects_list_finvasia = list(
            broker_creds_objects_finvasuia.values(
                "totp_key",
                "access_token",
                userid=F('user_id'),
            ),
        )

        accounts_finvasia = [
            {
                "userid": str(acc['userid']),
                "password": str(acc["totp_key"]),
                "access_token": str(acc["access_token"]),
            }
            for acc in broker_creds_objects_list_finvasia
        ]

        try:
            bot = FinvaciaTradingBot(
                accounts_finvasia=accounts_finvasia[0],
                req=req
            )

            bot.Buy()
        except Exception as e:
            print("error",e)

        return Response(data="hello")
