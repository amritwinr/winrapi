from brokers.tags import BROKER
from user.models import DnUseCaseMaster
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView


class SideBarView(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login
    )
    def get(self, request, *args, **kwargs):
        use_cases = DnUseCaseMaster.objects.filter(status="ACTIVE").values('id', 'use_case', 'icon','priority','url').order_by('priority')
        resp = []
        for use_case in use_cases:
            resp.append({
                "title": use_case['use_case'],
                "isHide": False,
                "icon": use_case['icon'],
                "link": use_case['url'],
            })
        return Response({"menu": resp})