from drf_yasg import openapi
from django.conf import settings
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.contrib import admin


schema_view = get_schema_view(
    openapi.Info(
        title="WinR APIs",
        default_version='v1',
        description="API documentation for WinR",
        contact=openapi.Contact(email="aditya@dotnitron.com"),
        license=openapi.License(name="Closed Source"),
    ),
   # url=settings.HOST_SERVER,
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
	path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/user/', include('user.urls')),
    path('api/broker/', include('brokers.urls')),
]