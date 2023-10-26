import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnRomilBroker
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        user = request.GET.get("user")
        brokerCredsObj = DnRomilBroker.objects.filter().values(
            'id', 'user', 'upper_level', 'upper_target', 'sl_upper', 'strike_ce', 'lower_level', 'lower_target', 'sl_lower', 'strike_pe', 'quantity', 'expiry',  'type', 'status', 'symbol', 'symbolNum')

        def get_table_keys():
            ins = DnRomilBroker()
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
        upper_level = data.get("upper_level", '')
        upper_target = data.get("upper_target", '')
        sl_upper = data.get("sl_upper", '')
        strike_ce = data.get("strike_ce", '')
        lower_level = data.get("lower_level", '')
        lower_target = data.get("lower_target", '')
        sl_lower = data.get("sl_lower", '')
        strike_pe = data.get("strike_pe", '')
        quantity = data.get("quantity", '')
        expiry = data.get("expiry", '')
        type = data.get("type", '')
        symbol = data.get("symbol", '')
        symbolNum = data.get("symbolNum", 0)

        obj = DnRomilBroker(user=user,
                            upper_level=upper_level,
                            upper_target=upper_target,
                            sl_upper=sl_upper,
                            strike_ce=strike_ce,
                            lower_level=lower_level,
                            lower_target=lower_target,
                            sl_lower=sl_lower,
                            strike_pe=strike_pe,
                            quantity=quantity,
                            expiry=expiry,
                            type=type,
                            symbol=symbol,
                            symbolNum=symbolNum,
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

        id = data.get("id", "")
        to_update = data.get("to_update", {})

        print(to_update)
        print(id)

        if not to_update or not id:
            raise Exception(12006)

        credObj = DnRomilBroker.objects.filter(id=id)
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

        credObj = DnRomilBroker.objects.filter(id=id)
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

        credObj = DnRomilBroker.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12008)

        credObj.update(quantity=quantity)
        return Response(status=200)
