from django.apps import AppConfig

class MediakitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mediakit'

    def ready(self):
        import mediakit.templatetags.mediakit_filters