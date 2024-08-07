from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .jobs import *

scheduler = None

def start():
	global scheduler
	scheduler = BackgroundScheduler()
	trigger = CronTrigger(hour=23, minute=59, second=0)
	scheduler.add_job(update_arcgis, trigger=trigger)
	scheduler.start()
