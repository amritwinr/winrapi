import jwt
import json
from django import db
from rest_framework import authentication
from user.models import DnUserMaster, DnAdminMaster, DnBrokerMaster


# class PostLoginAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth = None
#         try:
#             db.connections.close_all()
#             userToken = request.headers.get("jwtToken","")
#             userId = request.headers.get("userId","")
#             if userToken.startswith("b'") and userToken.endswith("'"):
#                 userToken = userToken[2:-1]
#             try:
#                 jwt.decode(userToken,'ADITYA-SECRET',algorithms=['HS256'])
#             except:
#                 raise Exception(11001)
            
#             if not userId:
#                 raise Exception(11002)
#             try:
#                 user = DnUserMaster.objects.get(id= int(userId))
#             except DnUserMaster.DoesNotExist:
#                 raise Exception(11003)
            
#             broker_name=""
#             if request.method in ['GET']:
#                 broker_name = request.GET.get('broker_name')
#             else:
#                 request_data = request.body.decode('utf-8')
#                 data = json.loads(request_data)
#                 broker_name = data.get("broker_name", "")

#             try:
#                 brokerObj=DnBrokerMaster.objects.get(name__iexact=broker_name)
#                 broker = brokerObj.pk
#             except DnBrokerMaster.DoesNotExist:
#                 broker = -1
            
#             request.userid = int(userId)
#             request.brokerid = broker
#             return "ok"
#         except Exception as e:
#             raise Exception(str(e))


import json
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

class PostLoginAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            db.connections.close_all()
            userToken = request.headers.get("jwtToken", "")
            userId = request.headers.get("userId", "")
            if userToken.startswith("b'") and userToken.endswith("'"):
                userToken = userToken[2:-1]
            
            try:
                jwt.decode(userToken, 'ADITYA-SECRET', algorithms=['HS256'])
            except:
                raise AuthenticationFailed("Invalid JWT token")

            if not userId:
                raise AuthenticationFailed("User ID is missing")
            
            try:
                user = DnUserMaster.objects.get(id=int(userId))
            except DnUserMaster.DoesNotExist:
                raise AuthenticationFailed("User not found")
            
            broker_name = ""
            if request.method == 'GET':
                broker_name = request.GET.get('broker_name')
            else:
                try:
                    request_data = request.body.decode('utf-8')
                    data = json.loads(request_data)
                    broker_name = data.get("broker_name", "")
                except json.JSONDecodeError:
                    raise AuthenticationFailed("Invalid JSON data")

            try:
                brokerObj = DnBrokerMaster.objects.get(name__iexact=broker_name)
                broker = brokerObj.pk
            except DnBrokerMaster.DoesNotExist:
                broker = -1

            request.userid = int(userId)
            request.brokerid = broker
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed(str(e))



class AdminAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = None
        try:
            db.connections.close_all()
            userToken = request.headers.get("jwtToken","")
            userId = request.headers.get("userId","")
            if userToken.startswith("b'") and userToken.endswith("'"):
                userToken = userToken[2:-1]
            try:
                jwt.decode(userToken,'ADITYA-SECRET',algorithms=['HS256'])
            except:
                raise Exception(11001)
            
            if not userId:
                raise Exception(11002)
            try:
                user = DnAdminMaster.objects.get(id= int(userId))
            except DnAdminMaster.DoesNotExist:
                raise Exception(11003)
            
            request.userid = int(userId)
            return "ok"
        except Exception as e:
            raise Exception(str(e))