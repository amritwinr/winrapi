import re
import random
import string
from drf_yasg import openapi
from datetime import datetime
from django.conf import settings
from django.utils import timezone

error_code =settings.ERROR_JSON
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_error_msg(code=0):
    return error_code.get(str(code), "Something went wrong")

def get_now_time():
    return datetime.now(tz=timezone.utc)

def camel_case_to_snake_case(str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def valid_serializer(serializer, error_code=None):
    if serializer.is_valid():
        return serializer.data
    if error_code is not None:
        raise Exception(error_code)
    for x, y in serializer.errors.items():
        error = str(x) + ' : ' + str(y)
        raise Exception(error)

def create_swagger_params(name, required=True, type='string',header_type="header",extra={}):
    swagger_type = openapi.TYPE_STRING
    header = openapi.IN_HEADER
    if type == "int":
        swagger_type = openapi.TYPE_INTEGER
    elif type == "bool":
        swagger_type = openapi.TYPE_BOOLEAN
    
    if header_type=="query":
        header=openapi.IN_QUERY
    return openapi.Parameter(name, header, type=swagger_type, required=required,**extra)

def check_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def generate_token(token_length=24):
    valid_chars = string.ascii_lowercase + string.digits + '-'
    token = random.choice(string.ascii_lowercase + string.digits)
    while len(token) < token_length:
        token += random.choice(valid_chars)
    token += random.choice(string.ascii_lowercase + string.digits)
    return token

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password
    
email = create_swagger_params(name="email", type="string",header_type="header")
username = create_swagger_params(name="username", type="string",header_type="header")
password = create_swagger_params(name="password", type="string",header_type="header")
engagement = create_swagger_params(name="engagement", type="string",header_type="header", required=False)
project = create_swagger_params(name="project", type="string",header_type="header", required=False)
userId = create_swagger_params(name="userId", type="int",header_type="header")
token = create_swagger_params(name="token", type="string",header_type="header")
newToken = create_swagger_params(name="newToken", type="string",header_type="header")
jwtToken = create_swagger_params(name="jwtToken", type="string",header_type="header")


login = [username,password,project]
admin_login = [email,password]
user_login = [email,password,engagement,project]
post_login = [userId,jwtToken]
post_upload = [userId,jwtToken,token]
admin_post_login = [userId,jwtToken]
new_user = [userId,newToken]