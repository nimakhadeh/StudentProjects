from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    label = 'my_notifications'  # ← این خط رو اضافه کن (اسم منحصر به فرد)