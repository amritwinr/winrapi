import json
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import DnBrokerUserStatusMaster
from custom_lib.api_view_class import PostLoginAPIView


class BrokerStatusView(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login
    )
    def post(self, request, *args, **kwargs):
        user_id = request.userid
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)
        
        broker_id = data.get("broker_id","")
        if not broker_id:
            raise Exception(12006)
        broker_id=int(broker_id)
        try:
            user_broker_status = DnBrokerUserStatusMaster.objects.get(broker_id=broker_id, user_id=user_id)
            if user_broker_status.status == 0:
                user_broker_status.status = 1
            else:
                user_broker_status.status = 0
            user_broker_status.save()
        except DnBrokerUserStatusMaster.DoesNotExist:
            DnBrokerUserStatusMaster(broker_id=broker_id, user_id=user_id, status=1).save()

        return Response("success")