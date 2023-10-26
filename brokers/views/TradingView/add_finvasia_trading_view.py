import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnFinvasiaTradingView
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        user = request.GET.get("user")
        brokerCredsObj = DnFinvasiaTradingView.objects.filter(user=user).values(
            'id', 'user', 'buy_sell', 'symbol', 'exchange', 'strike_price', 'strike_ce', 'strike_pe', 'strike_type', 'quantity', 'expiry', 'market_type', 'edge_size', 'target', 'stoploss',  'status')

        def get_table_keys():
            ins = DnFinvasiaTradingView()
            keys = [field.name for field in ins._meta.get_fields()
                    if not field.is_relation]
            return keys

        return Response(data=[list(brokerCredsObj), get_table_keys()])

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request):
        try:
            request_data = request.body.decode('utf-8')
            data = json.loads(request_data)
        except json.JSONDecodeError as e:
            # Handle JSON parsing error here
            raise ParseError(detail="Invalid JSON format")
        # request_data = request.body.decode('utf-8')
        # data = json.loads(request_data)
        user = data.get("user", '')
        buy_sell = data.get("buy_sell", '')
        symbol = data.get("symbol", '')
        exchange = data.get("exchange", '')
        strike_price = data.get("strike_price", '')
        strike_ce = data.get("strike_ce", '')
        strike_pe = data.get("strike_pe", '')
        strike_type = data.get("strike_type", '')
        quantity = data.get("quantity", '')
        expiry = data.get("expiry", '')
        market_type = data.get("market_type", '')
        edge_size = data.get("edge_size", '')
        target = data.get("target", '')
        stoploss = data.get("stoploss", '')
        status = data.get("status", '')

        obj = DnFinvasiaTradingView(user=user,
                                    buy_sell=buy_sell,
                                    symbol=symbol,
                                    exchange=exchange,
                                    strike_price=strike_price,
                                    strike_ce=strike_ce,
                                    strike_pe=strike_pe,
                                    strike_type=strike_type,
                                    quantity=quantity,
                                    expiry=expiry,
                                    market_type=market_type,
                                    edge_size=edge_size,
                                    target=target,
                                    stoploss=stoploss,
                                    status=status,
                                    )
        obj.save()
        id = obj.pk
        return Response({"id": id})

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def put(self, request):
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)
        updateType = data.get("updateType", "")

        if updateType == "many":
            new_status = data.get("status", "")
            DnFinvasiaTradingView.objects.all().update(status=new_status)
            return Response({"new_status": new_status})
        else:
            id = data.get("id", "")
            to_update = data.get("to_update", {})

            if not to_update or not id:
                raise Exception(12006)

            credObj = DnFinvasiaTradingView.objects.filter(id=id)
            if not credObj.exists():
                raise Exception(12020)

            credObj.update(**to_update)
            return Response({"id": id})

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def delete(self, request):
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)

        id = data.get("id", "")
        if not id:
            raise Exception(12006)

        credObj = DnFinvasiaTradingView.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12020)
        credObj.delete()
        return Response({"id": id})


class AddBrokerQuantityView(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request):
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)
        id = data.get("id", "")
        quantity = data.get("quantity", 0)

        if not id:
            raise Exception(12006)

        credObj = DnFinvasiaTradingView.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12008)

        credObj.update(quantity=quantity)
        return Response(status=200)
