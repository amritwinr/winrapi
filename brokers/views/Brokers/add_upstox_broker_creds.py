import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnUpstoxUserCredsMaster
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        user = request.GET.get("user")

        brokerCredsObj = DnUpstoxUserCredsMaster.objects.filter(user=user).values(
            'id', 'user', 'user_id', 'api_key', 'quantity', 'pin', 'mobile_no', 'secret_key', 'totp_key', 'status')

        def get_table_keys():
            ins = DnUpstoxUserCredsMaster()
            keys = [field.name for field in ins._meta.get_fields()
                    if not field.is_relation]
            return keys

        print(get_table_keys())

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

        user = data.get("user", '')
        print({"user-----": user})
        user_id = data.get("user_id", '')
        api_key = data.get("api_key", '')
        totp_key = data.get("totp_key", '')
        pin = data.get("pin", '')
        mobile_no = data.get("mobile_no", '')
        secret_key = data.get("secret_key", '') 

        if not user_id or not totp_key:
            raise Exception(12006)

        obj = DnUpstoxUserCredsMaster(user_id=user_id,
                                      user=user,
                                      api_key=api_key,
                                      totp_key=totp_key,
                                      pin=pin,
                                      mobile_no=mobile_no,
                                      secret_key=secret_key,
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
            DnUpstoxUserCredsMaster.objects.all().update(status=new_status)
            return Response({"new_status": new_status})
        else:
            id = data.get("id", "")
            to_update = data.get("to_update", {})

            print({"id------": id})

            if not to_update or not id:
                raise Exception(12006)

            credObj = DnUpstoxUserCredsMaster.objects.filter(id=id)
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

        credObj = DnUpstoxUserCredsMaster.objects.filter(id=id)
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

        credObj = DnUpstoxUserCredsMaster.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12008)

        credObj.update(quantity=quantity)
        return Response(status=200)
