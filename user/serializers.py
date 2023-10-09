from rest_framework import serializers
from custom_lib.base_serializer import BaseSerializer


class AdminRequestSerializer(BaseSerializer):
    id = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

class AdminRequestDeleteSerializer(BaseSerializer):
    request_id = serializers.IntegerField(required=True)

class AdSignUpSerializer(BaseSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=2, required=True)
    username = serializers.CharField(required=True)

class DeleteAdminSerializer(BaseSerializer):
    delete_user_id=serializers.IntegerField(required=True)

class SignUpSerializer(BaseSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

class AdminSignUpSerializer(BaseSerializer):
    username=serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    engagement = serializers.CharField(required=True)
    project = serializers.CharField(required=True)
    is_admin = serializers.IntegerField(required=True)

class UpdateUserSerializer(BaseSerializer):
    to_update = serializers.DictField(required=True)
    update_user_id=serializers.IntegerField(required=True)

class DeleteUserSerializer(BaseSerializer):
    delete_user_id=serializers.IntegerField(required=True)

class LoginSerializer(BaseSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class AdminLoginSerializer(BaseSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class RequestAccessSerializer(BaseSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    message = serializers.CharField(required=False)


class VerifyUserSerializer(BaseSerializer):
    email = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    
class ResendEmailSerializer(BaseSerializer):
    email = serializers.CharField(required=True)