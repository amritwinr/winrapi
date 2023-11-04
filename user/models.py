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
    user = models.CharField(max_length=1000)
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
    user = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    otpToken = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    vc = models.CharField(max_length=1000)
    app_key = models.CharField(max_length=1000)
    imei = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    unique_code = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_finvasia_user_creds_master'


class DnAngelUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    api_key = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    otpToken = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_angel_user_creds_master'


class DnUpstoxUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    api_key = models.CharField(max_length=1000)
    secret_key = models.CharField(max_length=1000)
    pin = models.CharField(max_length=1000)
    mobile_no = models.CharField(max_length=1000)
    totp_key = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_upstox_user_creds_master'


class DnFyersUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    fy_id = models.CharField(max_length=1000)
    app_id = models.CharField(max_length=1000)
    secret_key = models.CharField(max_length=1000)
    pin = models.CharField(max_length=1000)
    totp_key = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_fyers_creds_master'


class DnFlattradeUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    api_key = models.CharField(max_length=1000)
    secret_key = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    totp_key = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_flattrade_creds_master'


class Dn5paisaUserCredsMaster(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    app_name = models.CharField(max_length=1000)
    app_source = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    user_key = models.CharField(max_length=1000)
    encryption_key = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    passwd = models.CharField(max_length=1000)
    dob = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    is_main = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_5paisa_creds_master'


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


class DnRomilBroker(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    upper_level = models.CharField(max_length=1000)
    upper_target = models.CharField(max_length=1000)
    sl_upper = models.CharField(max_length=1000)
    strike_ce = models.CharField(max_length=1000)
    lower_level = models.CharField(max_length=1000)
    lower_target = models.CharField(max_length=1000)
    sl_lower = models.CharField(max_length=1000)
    strike_pe = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    expiry = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    symbol = models.CharField(max_length=1000)
    symbolNum = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'romil_broker'


class DnFinvasiaTradingView(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    buy_sell = models.CharField(max_length=1000)
    symbol = models.CharField(max_length=1000)
    exchange = models.CharField(max_length=1000)
    strike_price = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    strike_ce = models.CharField(max_length=1000)
    strike_pe = models.CharField(max_length=1000)
    strike_type = models.CharField(max_length=1000)
    expiry = models.CharField(max_length=1000)
    market_type = models.CharField(max_length=1000)
    edge_size = models.CharField(max_length=1000)
    target = models.CharField(max_length=1000)
    stoploss = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_finvasia_trading_view'


class DnTelegram(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    isAuthorized = models.BooleanField(default=False)
    code = models.CharField(max_length=1000)
    api_id = models.CharField(max_length=1000)
    api_hash = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_telegram'


class DnSubscribe(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    amount = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_subscribe'


class DnTelegramSubscribe(BaseFields):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    symbols = models.CharField(max_length=1000)

    class Meta:
        # managed = False
        db_table = 'dn_telegram_subscribe'
