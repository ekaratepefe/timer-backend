from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_mail_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_attempts = models.PositiveIntegerField(default=3)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment by {self.user.username} - {self.amount} USD'
