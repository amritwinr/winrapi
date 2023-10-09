from django.db import models


class BaseFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DnUserMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=500)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=1000)
    is_first = models.IntegerField(default=0)
    timestamp = models.CharField(max_length=255)

    class Meta:
       # managed = False
        db_table = 'dn_user_master'


class DnAdminMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=1000)

    class Meta:
       # managed = False
        db_table = 'dn_admin_master'


class DnUserRequestMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=500)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    otp = models.IntegerField()
    is_approved = models.IntegerField(default=0)

    class Meta:
       # managed = False
        db_table = 'dn_user_request_master'


class DnBrokerMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=10)

    class Meta:
        # managed = False
        db_table = 'dn_broker_master'


class DnBrokerUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    broker_id = models.BigIntegerField()
    broker_user_id = models.BigIntegerField()
    broker_api_key = models.CharField(max_length=1000)
    two_fa = models.CharField(max_length=1000)
    broker_name = models.CharField(max_length=1000)
    totp_encrypt_key = models.CharField(max_length=1000)
    quantity = models.IntegerField(default=0)
    is_main = models.IntegerField(default=0)
    do_twofa = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    is_background_task_running = models.BooleanField(default=False)

    class Meta:
        # managed = False
        db_table = 'dn_broker_user_creds_master'


class DnFinvasiaUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=1000)
    broker_id = models.CharField(max_length=1000)
    broker_user_id = models.CharField(max_length=1000)
    broker_name = models.CharField(max_length=1000)
    totp_encrypt_key = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    twoFA = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    vc = models.CharField(max_length=1000)
    app_key = models.CharField(max_length=1000)
    imei = models.CharField(max_length=1000)
    is_background_task_running = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'dn_finvasia_user_creds_master'


class DnUseCaseMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    use_case = models.CharField(max_length=500)
    icon = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=10, default="ACTIVE")
    priority = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'dn_use_case_master'


class DnBrokerUserStatusMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    broker_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    status = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'dn_broker_user_status_master'
