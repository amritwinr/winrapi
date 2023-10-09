from django.urls import path

from user.views.user_management import (user_request,
                                        user_login,
                                        user_pass,
)

from user.views.admin_management import (admin_user_request,
                                         create_admin,
)
from user.views.user_management.verify_user import ResendEmailView, VerifyUserView


# app_name = 'user'
urlpatterns = [
    # admin management endpoints
    path('admin_user_request', admin_user_request.AdminUserRequestView.as_view(), name='admin-user-request'),
    path('create_admin', create_admin.CreateAdminView.as_view(), name='create-admin'),


    # user management endpoints
    path('user_request', user_request.UserRequestView.as_view(), name='user-request'),
    path('login', user_login.LoginView.as_view(), name='user-login'),
    path('admin_login', user_login.AdminLoginView.as_view(), name='admin-login'),
    path('new_pass', user_pass.NewPasswordView.as_view(), name='new-password'),
    path('verify-email', VerifyUserView.as_view(), name='verify-email'),

    path('resend-email', ResendEmailView.as_view(), name='resend-email'),
]