import random
from datetime import timedelta
from django.utils import timezone
from vault.models import UserOTP



def generate_otp(user):
    code = str(random.randint(100000, 999999))
    expires = timezone.now() + timedelta(minutes=5)
    UserOTP.objects.update_or_create(user=user, defaults={"code": code, "expires_at": expires})
    return code

