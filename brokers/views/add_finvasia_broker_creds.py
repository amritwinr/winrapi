import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnFinvasiaUserCredsMaster
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        broker_id = request.brokerid
        user_id = request.userid
        if broker_id == -1:
            raise Exception(12012)

        brokerCredsObj = DnFinvasiaUserCredsMaster.objects.filter(user_id=user_id, broker_id=broker_id).values(
            'id', 'broker_user_id', 'twoFA', 'quantity','totp_encrypt_key', 'status', 'vc', 'app_key', 'imei', 'is_background_task_running')
        return Response(list(brokerCredsObj))

    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request):
        user_id = request.userid
        broker_id = request.brokerid
        # if broker_id == -1:
        #     raise Exception(12012)
        try:
            request_data = request.body.decode('utf-8')
            data = json.loads(request_data)
        except json.JSONDecodeError as e:
            # Handle JSON parsing error here
            raise ParseError(detail="Invalid JSON format")
        # request_data = request.body.decode('utf-8')
        # data = json.loads(request_data)
        broker_user_id = data.get("broker_user_id", '')
        broker_name = data.get("broker_name", '')

        twoFA = data.get("twoFA", '')
        totp_encrypt_key = data.get("totp_encrypt_key", '')
        vc = data.get("vc", '')
        app_key = data.get("app_key", '')
        imei = data.get("imei", '')

        if not broker_user_id or not twoFA or not totp_encrypt_key:
            raise Exception(12006)
        # if int(is_main) not in [0,1]:
        #     raise Exception()

        obj = DnFinvasiaUserCredsMaster(user_id=user_id,
                                      broker_name=broker_name,
                                      broker_id=broker_id,
                                      broker_user_id=broker_user_id,
                                      twoFA=twoFA,
                                      totp_encrypt_key=totp_encrypt_key,
                                      vc=vc,
                                      app_key=app_key,
                                      imei=imei,
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
            DnFinvasiaUserCredsMaster.objects.all().update(status=new_status)
            return Response({"new_status": new_status})
        else:
            id = data.get("id", "")
            to_update = data.get("to_update", {})

            if not to_update or not id:
                raise Exception(12006)

            credObj = DnFinvasiaUserCredsMaster.objects.filter(id=id)
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

        credObj = DnFinvasiaUserCredsMaster.objects.filter(id=id)
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

        credObj = DnFinvasiaUserCredsMaster.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12008)

        credObj.update(quantity=quantity)
        return Response(status=200)
