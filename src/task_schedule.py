from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

tz = timezone('Asia/Tehran')
scheduler = BackgroundScheduler(tz)


@scheduler.scheduled_job('interval', minutes=20)
def Task1():
    print('Task executed every 20min')


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=14, minute=0)
def Task2():
    print('Task executed every day at 14:00')


if __name__ == '__main__':
    scheduler.start()

    while True:
        # another process running in the main thread
        pass
