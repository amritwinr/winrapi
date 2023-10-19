import logging

from celery import shared_task
from django.db.models import F
import datetime

from brokers.helper.aliceblue.copy_trade import TradingBot
from brokers.helper.finvasia.copy_trade import FinvaciaBot
from user.models import DnBrokerUserCredsMaster
import threading

@shared_task()
def place_order_by_master_task(broker_creds_obj, master_id):
    accounts = [
        {"userid": str(acc['userid']), "api_key": str(
            acc['api_key']), "Qty": str(acc['quantity'])}
        for acc in broker_creds_obj
    ]
    try:
        bot = TradingBot(
            master_account=accounts[0],
            other_accounts=accounts[1:],
            logger=logging.getLogger('place_order_by_master_task')
        )
        bot.fetch_master_session_id()
        bot.order_history_df, bot.num_rows1 = bot.fetch_order_history()
        print(bot.order_history_df.shape)
        bot.process_orders()
    except Exception as e:
        print(f'Error :: {e}')
        place_order_by_master_task.delay(broker_creds_obj, master_id)
        return

    master = DnBrokerUserCredsMaster.objects.get(id=master_id)
    master.is_background_task_running = False
    master.save()


@shared_task()
def place_order_by_Finvasia_master_task(broker_creds_obj, master_id, user):
    accounts = [
        {
         "userid": str(acc['userid']),
         "app_key": str(acc['app_key']),
         "Qty": str(acc['quantity']),
         "twoFA": str(acc["twoFA"]),
         "password": str(acc["totp_key"]),
         "vc": str(acc["vc"]),
         "imei": str(acc["imei"]),
         "access_token": str(acc["access_token"]),
         }
        for acc in broker_creds_obj
    ]

    try:
        bot = FinvaciaBot(
            master_account=accounts[0],
            other_accounts=accounts[1:],
            logger=logging.getLogger('place_order_by_master_task'),
            user=user
        )
        print(datetime.datetime.now())
        # bot.order_history_df, bot.num_rows1 = bot.get_order_book()
        target=bot.process_orders()

    except Exception as e:
        print(f'Error :: {e}')
        # place_order_by_Finvasia_master_task.delay(broker_creds_obj, master_id)
        return
