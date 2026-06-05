from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# 📅 DAILY RECORD
class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# 💰 EARNINGS
class Earning(models.Model):
    record = models.ForeignKey(
        DailyRecord,
        on_delete=models.CASCADE,
        related_name="earnings"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client_name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    amount = models.FloatField()


# 📂 EXPENSE CATEGORY (DYNAMIC)
class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 💸 EXPENDITURE
class Expenditure(models.Model):
    record = models.ForeignKey(
        DailyRecord,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    location = models.CharField(max_length=255)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.title} - {self.amount}"
    
