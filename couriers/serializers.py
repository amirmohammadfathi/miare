from rest_framework import serializers
from django.db.models import Sum

from couriers.models import Courier, Trip, AdditionalEarning, WeeklyEarning, DailyEarning
from core.celery import celery_app


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['id', 'first_name', 'last_name']


class TripSerializer(serializers.ModelSerializer):
    daily_income = serializers.SerializerMethodField()
    courier = serializers.SerializerMethodField()

    def get_courier(self, obj: Trip) -> dict:
        courier = obj.courier
        return CourierSerializer(courier).data

    def get_daily_income(self, obj: Trip) -> float:
        task_result = celery_app.send_task(
            "couriers.tasks.update_daily_earning", args=(obj.courier.id, obj.income), kwargs={"income_type": 'trip'}
        )
        updated_daily_income = task_result.get()

        return updated_daily_income

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['courier', 'id', 'date']


class AdditionalEarningSerializer(serializers.ModelSerializer):
    daily_income = serializers.SerializerMethodField()
    courier = serializers.SerializerMethodField()

    def get_courier(self, obj: AdditionalEarning) -> dict:
        courier = obj.courier
        return CourierSerializer(courier).data

    def get_daily_income(self, obj: AdditionalEarning) -> float:
        income_type = {"income_type": 'award' if obj.is_for_award else 'punishment'}
        task_result = celery_app.send_task(
            "couriers.tasks.update_daily_earning", args=(obj.courier.id, obj.amount), kwargs=income_type
        )
        updated_daily_income = task_result.get()
        return updated_daily_income

    class Meta:
        model = AdditionalEarning
        fields = '__all__'
        read_only_fields = ['courier', 'id', 'date']


class DailyEarningSerializer(serializers.ModelSerializer):
    courier = serializers.SerializerMethodField()

    def get_courier(self, obj: DailyEarning) -> dict:
        return CourierSerializer(obj.courier).data

    class Meta:
        model = DailyEarning
        fields = '__all__'
        read_only_fields = ['courier', 'id', 'date']


class WeeklyEarningSerializer(serializers.ModelSerializer):
    courier = serializers.SerializerMethodField()
    earnings = serializers.SerializerMethodField()

    def get_courier(self, obj: WeeklyEarning) -> dict:
        courier = obj.courier
        return CourierSerializer(courier).data

    def get_earnings(self, obj: WeeklyEarning) -> float:
        weekly_earning = (
            obj.courier.courier_daily_earning
            .filter(date__range=[obj.from_date, obj.to_date])
            .aggregate(earnings=Sum('earnings'))['earnings']
        )
        return weekly_earning if weekly_earning else 0

    def save(self, **kwargs):
        self.instance.earnings = self.get_earnings(self.instance)
        super().save(update_fields=['earnings'], **kwargs)

    class Meta:
        model = WeeklyEarning
        fields = '__all__'
        read_only_fields = ['courier', 'id']
