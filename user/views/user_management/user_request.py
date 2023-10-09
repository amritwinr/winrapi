import bcrypt
from user.email_check import send_email
from user.tags import USER
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.helper import valid_serializer
from custom_lib.api_view_class import CustomAPIView
from user.serializers import RequestAccessSerializer
from user.models import DnUserRequestMaster,DnUserMaster


class UserRequestView(CustomAPIView):
    @swagger_auto_schema(
        tags=[USER],
        request_body=RequestAccessSerializer
    )
    def post(self, request):
        data = valid_serializer(RequestAccessSerializer(data=request.data), error_code=12006)
        email = data["email"]
        phone = data["phone"]
        username = data["username"]
        password = data["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        message = data.get("message","")
        
        user_exists = DnUserMaster.objects.filter(email__iexact=email).exists()
        if user_exists:
             return Response({"errorMessage" : " Email Already Exists","errorCode" : 1})
        user_exists = DnUserMaster.objects.filter(username__iexact=username).exists()
        if user_exists:
             return Response({"errorMessage" : "UserName Already Exists","errorCode" : 2})
        user_exists = DnUserMaster.objects.filter(phone__iexact=phone).exists()
        if user_exists:
             return Response({"errorMessage" : "Phone Already Exists","errorCode" : 3})
        user_exists = DnUserMaster.objects.filter(email__iexact=email, username__iexact=username, phone__iexact=phone).exists()
        if user_exists:
             return Response({"errorMessage" : "User  Already Exists","errorCode" : 4})

        DnUserMaster.objects.create(email=email, username=username, phone=phone,password=hashed_password.decode('utf-8'))
        otp = send_email(email)
        DnUserRequestMaster.objects.create(email=email, username=username, phone=phone, otp=otp)
       
        return Response("Access Requested Successfully!!")