from brokers.tags import BROKER
from custom_lib.helper import post_login
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import PostLoginAPIView
from rest_framework.exceptions import ParseError
import json
import pyotp
from .api_helper import ShoonyaApiPy
from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import parse_qs, urlparse, quote
import requests
from user.models import DnUpstoxUserCredsMaster, DnFinvasiaUserCredsMaster
from py5paisa import FivePaisaClient
from SmartApi import SmartConnect


class CheckCred(PostLoginAPIView):
    @swagger_auto_schema(
        tags=[BROKER],
        manual_parameters=post_login,
    )
    def post(self, request, *args, **kwargs):
        req = json.loads(request.body.decode("utf-8"))

        try:
            if req['type'] == "Finvasia":
                api = ShoonyaApiPy()
                factor2 = pyotp.TOTP(req['twoFA']).now()

                ret = api.login(userid=req['user_id'], password=req['totp_key'], twoFA=factor2,
                                vendor_code=req['vc'], api_secret=req['app_key'], imei=req['imei'])
                userToken = ret.get('susertoken')

                DnFinvasiaUserCredsMaster.objects.filter(id=req["id"]).update(
                    access_token=userToken)
                return Response(status=200)

            elif req["type"] == "Angel One":

                obj = SmartConnect(api_key=req["api_key"])
                factor1 = pyotp.TOTP(req["twoFA"]).now()

                # login api call
                data = obj.generateSession(
                    req["user_id"], req["totp_key"], factor1)
                refreshToken = data['data']['refreshToken']

                # fetch the feedtoken
                feedToken = obj.getfeedToken()

                # fetch User Profile
                userProfile = obj.getProfile(refreshToken)

                if userProfile["message"] == "SUCCESS":
                    return Response(data={"message": "Success"}, status=200)
                else:
                    return Response(data={"message": "Faile"}, status=400)

            elif req["type"] == "Upstox":

                RURL = 'https://apix.stocksdeveloper.in/oauth/upstox'
                rurlEncode = quote(RURL, safe="")
                AUTH_URL = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={req["api_key"]}&redirect_uri={rurlEncode}'

                def getAccessToken(code):
                    url = 'https://api-v2.upstox.com/login/authorization/token'

                    headers = {
                        'accept': 'application/json',
                        'Api-Version': '2.0',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }

                    data = {
                        'code': code,
                        'client_id': req["api_key"],
                        'client_secret': req["secret_key"],
                        'redirect_uri': RURL,
                        'grant_type': 'authorization_code'
                    }

                    response = requests.post(url, headers=headers, data=data)
                    json_response = response.json()
                    
                    return json_response

                def run(playwright: Playwright) -> str:
                    browser = playwright.chromium.launch(headless=True)
                    context = browser.new_context()
                    page = context.new_page()
                    with page.expect_request(f"*{RURL}?code*") as request:
                        page.goto(AUTH_URL)
                        page.locator("#mobileNum").click()
                        page.locator("#mobileNum").fill(req["mobile_no"])
                        page.get_by_role("button", name="Get OTP").click()
                        page.locator("#otpNum").click()
                        otp = pyotp.TOTP(req["totp_key"]).now()
                        page.locator("#otpNum").fill(otp)
                        page.get_by_role("button", name="Continue").click()
                        page.get_by_label("Enter 6-digit PIN").click()
                        page.get_by_label("Enter 6-digit PIN").fill(req["pin"])
                        res = page.get_by_role(
                            "button", name="Continue").click()
                        page.wait_for_load_state()

                    url = request.value.url
                    print(f"Redirect Url with code : {url}")
                    parsed = urlparse(url)
                    code = parse_qs(parsed.query)['code'][0]
                    context.close()
                    browser.close()
                    return code
                with sync_playwright() as playwright:
                    code = run(playwright)
                access_token = getAccessToken(code)
                print(access_token)

                DnUpstoxUserCredsMaster.objects.filter(id=req["id"]).update(
                    access_token=access_token["access_token"])

                return Response(status=200)

            elif req["type"] == "5paisa":
                print(req)
                cred = {
                    "APP_NAME": req["app_name"],
                    "APP_SOURCE": req["app_source"],
                    "USER_ID": req["user_id"],
                    "PASSWORD": req["password"],
                    "USER_KEY": req["user_key"],
                    "ENCRYPTION_KEY": req["encryption_key"]
                }

                client = FivePaisaClient(
                    email=req["email"], passwd=req["passwd"], dob=req["dob"], cred=cred)
                client.login()

                print({"client -----------------" : client})
                return Response(status=200)

        except:
            return Response(status=400)
