from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .jobs import *

scheduler = None

def start():
	global scheduler
	scheduler = BackgroundScheduler()
	trigger_tramites = CronTrigger(hour=23, minute=59, second=0)
	trigger_estaciones = CronTrigger(minute='*/5')
	scheduler.add_job(update_tramites_arcgis, trigger=trigger_tramites)
	scheduler.add_job(update_estaciones_arcgis, trigger=trigger_estaciones)
	scheduler.start()
