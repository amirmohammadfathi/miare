from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator
from datetime import date
import uuid


class Courier(AbstractBaseUser):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = None
    last_login = None

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return str(self.id)


class Trip(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    courier = models.ForeignKey(Courier, related_name='courier', on_delete=models.CASCADE)

    income = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    date = models.DateField(default=date.today())
    distance = models.FloatField(null=True, blank=True)
    customer_type = models.CharField(max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class AdditionalEarning(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    courier = models.ForeignKey(Courier, related_name='courier_additional_earning', on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    date = models.DateField(default=date.today())
    is_for_award = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class DailyEarning(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    courier = models.ForeignKey(Courier, related_name='courier_daily_earning', on_delete=models.CASCADE)
    date = models.DateField(default=date.today(), editable=False)
    earnings = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class WeeklyEarning(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    courier = models.ForeignKey(Courier, related_name='courier_weekly_earning', on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    earnings = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
