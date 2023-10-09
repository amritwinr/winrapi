from NorenRestApiPy.NorenApi import NorenApi
from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError
import json
import pyotp
from .api_helper import ShoonyaApiPy

class CheckCred(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))
        print(req)

        for key, value in req.items():
            print(f"Key: {key}, Value: {value}")

        try:
            if req['type'] == "Finvasia":
                api = ShoonyaApiPy()
                factor2 = pyotp.TOTP(req['twoFA']).now()

                ret = api.login(userid=req['broker_user_id'], password=req['totp_encrypt_key'], twoFA=factor2, 
                                vendor_code=req['vc'], api_secret=req['app_key'], imei=req['imei'])
                print(ret["actid"])
                return Response(status=200)
            
            elif req["type"] == "Alice blue":
                 pass
        except:
                return Response(status=400)