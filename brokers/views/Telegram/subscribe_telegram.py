import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnTelegramSubscribe
from custom_lib.api_view_class import PostLoginAPIView


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        user = request.GET.get("user")
        print(user)
        brokerCredsObj = DnTelegramSubscribe.objects.filter(user=user).values(
            'id', 'user', 'quantity', 'name', 'symbols')

        return Response(data=list(brokerCredsObj))

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

        user = data.get("user", '')
        quantity = data.get("quantity", '')
        name = data.get("name", '')
        symbols = data.get("symbols", '')

        if not user:
            raise Exception(12006)
        # if int(is_main) not in [0,1]:
        #     raise Exception()

        obj = DnTelegramSubscribe(user=user,
                                     quantity=quantity,
                                     name=name,
                                     symbols=symbols,
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

        credObj = DnTelegramSubscribe.objects.filter(id=id)

        if not credObj.exists():
            raise Exception(12006)

        credObj = DnTelegramSubscribe.objects.filter(id=id)
        credObj.update(**to_update)
        return Response({"id": id})

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def delete(self, request):
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)

        print({"data": data})

        id = data.get("id", "")
        if not id:
            raise Exception(12006)

        credObj = DnTelegramSubscribe.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12020)
        credObj.delete()
        return Response({"id": id})
