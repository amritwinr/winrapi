import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnTelegram
from custom_lib.api_view_class import PostLoginAPIView


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        user = request.GET.get("user")
        print(user)
        brokerCredsObj = DnTelegram.objects.filter(user=user).values(
            'id', 'user', 'code', 'isAuthorized', 'api_id', 'api_hash', 'phone')

        return Response(data=list(brokerCredsObj))

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def put(self, request):
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)
        user = data.get("user", '')

        credObj = DnTelegram.objects.filter(user=user)

        if not credObj.exists():
            code = data.get("code", '')
            obj = DnTelegram(user=user, code=code)
            obj.save()
            id = obj.pk
            return Response({"id": id})

        else:
            id = data.get("id", "")
            credObj = DnTelegram.objects.filter(id=id)
            to_update = data.get("to_update", {})
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

        credObj = DnTelegram.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12020)
        credObj.delete()
        return Response({"id": id})
