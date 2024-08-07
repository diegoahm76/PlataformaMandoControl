from django.apps import AppConfig


class GeojsonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geojson'
    
    def ready(self):
        from jobs import  updater
        updater.start()
