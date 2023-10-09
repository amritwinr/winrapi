import time
import bcrypt
from user.tags import USER
from user.models import DnUserMaster
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from custom_lib.api_view_class import CustomAPIView
from user.serializers import ChangePasswordSerializer
from custom_lib.helper import new_user,valid_serializer


class NewPasswordView(CustomAPIView):
    @swagger_auto_schema(
        tags=[USER],
        manual_parameters=new_user,
        request_body=ChangePasswordSerializer
    )
    def post(self, request):
        data = valid_serializer(ChangePasswordSerializer(data=request.data), error_code=12006)
        old_pwd = data["old_password"]
        new_pwd = data["new_password"]
        token = request.headers.get('newToken', '')
        userId = request.headers.get('userId', '')
        if not token or not userId:
            raise Exception(12006)
        if not old_pwd or not new_pwd:
            raise Exception(12006)

        st = str(token).split("#&@*")
        newToken = st[0]
        timestamp = int(st[1])
        userObj = DnUserMaster.objects.filter(id=userId).first()
        if not userObj:
            raise Exception(12008)

        dt = userObj.timestamp.split("#&@*")
        storedNewToken = dt[0]
        storedTimestamp = int(dt[1])
        if storedTimestamp != timestamp or storedNewToken != newToken:
            raise Exception(12011)
        if storedTimestamp < int(time.time()):
            raise Exception(12011)
        if userObj.is_first != 0:
            raise Exception(12011)

        old_pwd = old_pwd.encode('utf-8')
        userBytes = userObj.password.encode('utf-8')
        result = bcrypt.checkpw(old_pwd, userBytes)
        if not result:
            raise Exception(12010)

        bytes = new_pwd.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        new_pwd = hash.decode('utf-8')
        userObj.password = new_pwd
        userObj.is_first = 1
        userObj.save()
        return Response({'message': 'Password has been changed successfully.'})