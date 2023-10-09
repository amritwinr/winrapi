import bcrypt
from user.tags import ADMIN
from user.models import DnAdminMaster
from rest_framework.response import Response
from custom_lib.helper import valid_serializer
from drf_yasg.utils import swagger_auto_schema
from user.serializers import AdSignUpSerializer
from custom_lib.api_view_class import CustomAPIView


class CreateAdminView(CustomAPIView):
    @swagger_auto_schema(
        tags=[ADMIN],
        request_body=AdSignUpSerializer
    ) 
    def post(self, request):
        data = valid_serializer(AdSignUpSerializer(data=request.data), error_code=12048)
        email = data["email"]
        password = data["password"]
        username = data["username"]
        userObj=DnAdminMaster.objects.filter(email=email)
        if userObj.exists():
            raise Exception(12009)
        
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        password = hash.decode('utf-8')
        user = DnAdminMaster(password=password,email=email,username=username)
        user.save()
        return Response("Admin created Successfully!")