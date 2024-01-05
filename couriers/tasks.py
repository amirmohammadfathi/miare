from celery import shared_task
from couriers.models import Courier, DailyEarning, WeeklyEarning
from datetime import date, timedelta
from django.db import transaction
from typing import Literal


@shared_task(name='couriers.tasks.create_daily_earning')
def create_daily_earning() -> None:
    couriers = Courier.objects.only("id").all()
    daily_earnings = [
        DailyEarning(courier=courier) for courier in couriers
    ]
    with transaction.atomic():
        DailyEarning.objects.bulk_create(daily_earnings)


@shared_task(name='couriers.tasks.update_daily_earning')
def update_daily_earning(
        courier_id: str, amount: float, income_type: Literal["trip", "punishment", "award"] = None
) -> float:
    with transaction.atomic():
        daily_earning = DailyEarning.objects.select_for_update().filter(courier_id=courier_id).only("earnings").first()
        daily_earning.earnings += amount if income_type in ["trip", "award"] else 0
        daily_earning.earnings -= amount if income_type == 'punishment' else 0
        daily_earning.save()
    return daily_earning.earnings


@shared_task(name='couriers.tasks.calculate_weakly_earning')
def create_weakly_earning() -> None:
    today = date.today()  # Saturday
    last_weak_saturday = today - timedelta(days=7)
    last_weak_friday = today - timedelta(days=1)
    couriers = Courier.objects.only("id")
    weakly_earning = [
        WeeklyEarning(courier=courier, from_date=last_weak_saturday, to_date=last_weak_friday, earnings=0.0)
        for courier in couriers
    ]
    with transaction.atomic():
        WeeklyEarning.objects.bulk_create(weakly_earning)
