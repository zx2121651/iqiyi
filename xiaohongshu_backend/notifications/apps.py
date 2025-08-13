from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "xiaohongshu_backend.notifications"

    def ready(self):
        import xiaohongshu_backend.notifications.signals
