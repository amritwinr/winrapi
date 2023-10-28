from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView
from user.models import DnBrokerMaster, DnBrokerUserStatusMaster


class BrokerListView(PostLoginAPIView): 
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login
    )
    def get(self, request, *args, **kwargs):
        user_id = request.userid
        active_brokers = DnBrokerMaster.objects.all()

        response_data = []
        for broker in active_brokers:
            try:
                user_broker_status = DnBrokerUserStatusMaster.objects.get(
                    broker_id=broker.id, user_id=user_id)
                user_status = user_broker_status.status
            except DnBrokerUserStatusMaster.DoesNotExist:
                user_status = -1

            broker_data = {
                'id': broker.id,
                'name': broker.name,
                'status': broker.status,
                'user_status': user_status
            }
            response_data.append(broker_data)

        return Response(response_data)
