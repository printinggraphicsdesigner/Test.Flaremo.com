from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            print("❌ ENV missing")
            return

        user, created = User.objects.get_or_create(username=username)

        user.email = email
        user.set_password(password)   # 🔥 IMPORTANT
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            print("✅ Superuser created")
        else:
            print("♻️ Superuser updated")
