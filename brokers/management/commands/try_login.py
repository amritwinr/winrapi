from django.core.management.base import BaseCommand
from brokers.helper.aliceblue.totp_login import AliceBlueClient
from user.models import DnBrokerUserCredsMaster, DnBrokerUserStatusMaster


class Command(BaseCommand):
    help = 'Tries to login for all user accounts'

    def handle(self, *args, **kwargs):
        userBrokerObj = DnBrokerUserStatusMaster.objects.filter(broker_id=2, status=1)
        for user in userBrokerObj:
            userCredObj=DnBrokerUserCredsMaster.objects.filter(do_twofa=1, broker_id=2, user_id=user.id)
            if not userCredObj.exists():
                continue
            for userCred in userCredObj:
                try:
                    broker_user_id = userCred.broker_user_id
                    broker_api_key = userCred.broker_api_key
                    two_fa = userCred.two_fa
                    totp_encrypt_key = userCred.totp_encrypt_key

                    client = AliceBlueClient(userId=broker_user_id,
                                            password=broker_api_key,
                                            two_fa=two_fa,
                                            totp_encrypt_key=totp_encrypt_key)
                    resp=client.login()
                    if resp=="success":
                        userCred.status=1
                    else:
                        userCred.status=0
                except:
                    userCred.status = 0
                userCred.save()

        self.stdout.write(self.style.SUCCESS('Login attempt complete for all users'))