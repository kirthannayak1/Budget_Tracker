from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_daily_waged = models.BooleanField(default=False)

    monthly_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )