from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView

from couriers.serializers import (
    CourierSerializer, TripSerializer, AdditionalEarningSerializer, WeeklyEarningSerializer, DailyEarningSerializer
)
from couriers.models import Courier, AdditionalEarning, DailyEarning, WeeklyEarning
from datetime import date, timedelta


class CreateListCouriers(CreateAPIView, ListAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()


class TripOfCourier(CreateAPIView):
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        serializer.save(courier_id=self.kwargs.get("pk"))


class AdditionalEarningOfCourier(CreateAPIView, ListAPIView):
    serializer_class = AdditionalEarningSerializer

    def perform_create(self, serializer):
        serializer.save(courier_id=self.kwargs.get("pk"))

    def get_queryset(self):
        return (
            AdditionalEarning.objects.filter(date=date.today(), courier_id=self.kwargs.get("pk"))
            .select_related('courier').all()
        )


class RetrieveCourierDailyEarning(RetrieveAPIView):
    serializer_class = DailyEarningSerializer

    def get_object(self):
        return (
            DailyEarning.objects.filter(date=date.today(), courier_id=self.kwargs.get("pk"))
            .select_related('courier').first()
        )


class RetrieveCourierWeeklyEarning(RetrieveAPIView):
    serializer_class = WeeklyEarningSerializer

    def get_object(self):
        today = date.today()  # Saturday
        last_weak_saturday = today - timedelta(days=7)
        last_weak_friday = today - timedelta(days=1)
        return (
            WeeklyEarning.objects.filter(
                from_date=last_weak_saturday, to_date=last_weak_friday, courier_id=self.kwargs.get("pk")
            ).select_related('courier').prefetch_related('courier__courier_daily_earning').first()
        )
