from django.contrib import admin
from .models import   *
# Register your models here.

admin.site.register(DnUserMaster)
admin.site.register(DnAdminMaster)
admin.site.register(DnUserRequestMaster)
admin.site.register(DnBrokerUserCredsMaster)
admin.site.register(DnUseCaseMaster)
admin.site.register(DnBrokerUserStatusMaster)
admin.site.register(DnBrokerMaster)

