import bcrypt
from user.email_check import send_email
from user.tags import USER
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.helper import valid_serializer
from custom_lib.api_view_class import CustomAPIView
from user.serializers import RequestAccessSerializer, ResendEmailSerializer, VerifyUserSerializer
from user.models import DnUserRequestMaster,DnUserMaster


class VerifyUserView(CustomAPIView):
    @swagger_auto_schema(
        tags=[USER],
        request_body=VerifyUserSerializer
    )
    def post(self, request):
        data = valid_serializer(VerifyUserSerializer(data=request.data), error_code=12006)
        email = data["email"]
        otp = data["otp"]
       
   
        user =  DnUserRequestMaster.objects.filter(email__iexact=email).first()
        print( otp)
        if user:
            if str(user.otp) == str(otp):
                user.is_approved = True
                user.save()
            else :
                raise Exception(12009)
        else: 
           raise Exception(12009)
        
        return Response("Email Verified Successfully!!")
    
    

class ResendEmailView(CustomAPIView):
    @swagger_auto_schema(
        tags=[USER],
        request_body=ResendEmailSerializer
    )
    def post(self, request):
        data = valid_serializer(ResendEmailSerializer(data=request.data), error_code=12006)
        email = data["email"]
       
   
        user = DnUserRequestMaster.objects.filter(email__iexact=email).first()
        if user:
            otp =send_email(email)
          
            user.otp = otp
            user.save()
        else: 
           raise Exception(12009)
        
        return Response("Email Resend Successfully!!")