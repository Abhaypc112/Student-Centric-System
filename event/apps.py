from django.apps import AppConfig


class eventConfig(AppConfig):
    name = 'event'
    def ready(self):
        import event.signals
        return super().ready()