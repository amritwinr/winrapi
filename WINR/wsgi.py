import os
from pytz import timezone
from datetime import datetime
from django.core.wsgi import get_wsgi_application

is_running = False
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WINR.settings')
application = get_wsgi_application()

from apscheduler.schedulers.background import BackgroundScheduler
from brokers.management.commands.do_trade import Command as TradeCommand
from brokers.management.commands.try_login import Command as TryLoginCommand


def run_login_job():
    cmd = TryLoginCommand()
    cmd.handle()


def run_your_command_job():
    global is_running
    if is_running:
        return

    current_time = datetime.now().astimezone(timezone("Asia/Kolkata")).time()
    start_time = datetime.strptime("09:00:00", "%H:%M:%S").time()
    end_time = datetime.strptime("22:00:00", "%H:%M:%S").time()

    try:
        is_running = True
        cmd = TradeCommand()
        cmd.handle()
    finally:
        is_running = False


scheduler = BackgroundScheduler()
scheduler.add_job(run_login_job, 'cron', hour=8, minute=0, timezone="Asia/Kolkata")
scheduler.add_job(run_your_command_job, 'interval', minutes=1, timezone="Asia/Kolkata")
scheduler.start()
