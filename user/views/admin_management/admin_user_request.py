import bcrypt
from user.tags import ADMIN
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import AdminAPIView
from user.serializers import AdminRequestSerializer, AdminRequestDeleteSerializer
from custom_lib.helper import admin_post_login,valid_serializer,generate_password,check_email
from user.models import DnUserMaster,DnUserRequestMaster,DnBrokerUserStatusMaster,DnBrokerMaster


class AdminUserRequestView(AdminAPIView):
    @swagger_auto_schema(
        tags=[ADMIN],
        manual_parameters=admin_post_login
    )
    def get(self, request):
        requestObj = DnUserRequestMaster.objects.filter(is_approved=0).values("id","email","username","phone","message")
        if not requestObj.exists():
            return Response({})
        
        return Response(list(requestObj))
    
    @swagger_auto_schema(
        tags=[ADMIN],
        manual_parameters= admin_post_login,
        request_body=AdminRequestSerializer
        )
    def post(self,request):
        data = valid_serializer(AdminRequestSerializer(data=request.data), error_code=12006)
        request_id = data["id"]
        email = data["email"]
        username = data["username"]
        phone = data["phone"]
        
        if not check_email(email):
            raise Exception(12007)

        userObj=DnUserMaster.objects.filter(username__iexact=username)
        if userObj.exists():
            raise Exception(12009)
        
        # password=generate_password()
        password="winr123"
        pwd=password
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        password = hash.decode('utf-8')
        user = DnUserMaster(username=username,password=password,email=email,phone=phone)
        user.save()
        user_id=user.pk
        brokerObj=DnBrokerMaster.objects.all()
        for broker in brokerObj:
            DnBrokerUserStatusMaster(user_id=user_id, broker_id=broker.id).save()
            
        userRequestObj=DnUserRequestMaster.objects.filter(id=int(request_id))
        userRequestObj.update(is_approved=1)
        return Response("User created successfully!")

    @swagger_auto_schema(
        tags=[ADMIN],
        manual_parameters= admin_post_login,
        request_body=AdminRequestDeleteSerializer
        )
    def delete(self,request):        
        data = valid_serializer(AdminRequestDeleteSerializer(data=request.data), error_code=12006)
        userRequestObj=DnUserRequestMaster.objects.filter(id=data["request_id"])
        userRequestObj.update(is_approved=2)
        return Response({"id":data["request_id"]})