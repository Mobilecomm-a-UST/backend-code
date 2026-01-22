from django.apps import AppConfig


class SoftAtRejectedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Soft_AT_Rejected'


    def ready(self):
        from Soft_AT_Rejected import signals
