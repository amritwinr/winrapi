import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import Dn5paisaUserCredsMaster
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError


class BrokerStore(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def get(self, request, *args, **kwargs):
        user = request.GET.get("user")
        brokerCredsObj = Dn5paisaUserCredsMaster.objects.filter(user=user).values(
            'id', 'user', 'user_id', 'app_name', 'app_source', 'password', 'user_key', 'encryption_key', 'email', 'passwd', 'dob', 'quantity',  'status')

        def get_table_keys():
            ins = Dn5paisaUserCredsMaster()
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
        user_id = data.get("user_id", '')
        app_name = data.get("app_name", '')
        app_source = data.get("app_source", '')
        password = data.get("password", '')
        user_key = data.get("user_key", '')
        encryption_key = data.get("encryption_key", '')
        email = data.get("email", '')
        passwd = data.get("passwd", '')
        dob = data.get("dob", '')

        if not user_id or not password:
            raise Exception(12006)

        obj = Dn5paisaUserCredsMaster(user=user,
                                      user_id=user_id,
                                      app_name=app_name,
                                      app_source=app_source,
                                      password=password,
                                      user_key=user_key,
                                      encryption_key=encryption_key,
                                      email=email,
                                      passwd=passwd,
                                      dob=dob,
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
            Dn5paisaUserCredsMaster.objects.all().update(status=new_status)
            return Response({"new_status": new_status})
        else:
            id = data.get("id", "")
            to_update = data.get("to_update", {})

            if not to_update or not id:
                raise Exception(12006)

            credObj = Dn5paisaUserCredsMaster.objects.filter(id=id)
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

        credObj = Dn5paisaUserCredsMaster.objects.filter(id=id)
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

        credObj = Dn5paisaUserCredsMaster.objects.filter(id=id)
        if not credObj.exists():
            raise Exception(12008)

        credObj.update(quantity=quantity)
        return Response(status=200)
