from datetime import timedelta, date

import factory.fuzzy

from couriers.models import Trip, Courier, AdditionalEarning, DailyEarning, WeeklyEarning


class CourierFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("pystr")
    last_name = factory.Faker("pystr")

    class Meta:
        model = Courier


class TripFactory(factory.django.DjangoModelFactory):
    courier = factory.SubFactory(CourierFactory)
    customer_type = factory.Faker("pystr")
    income = factory.Faker('pyfloat', positive=True)

    class Meta:
        model = Trip


class AdditionalEarningFactory(factory.django.DjangoModelFactory):
    courier = factory.SubFactory(CourierFactory)
    amount = factory.Faker('pyfloat')
    reason = factory.Faker('pystr')
    is_for_award = factory.Faker('pybool')

    class Meta:
        model = AdditionalEarning


class DailyEarningFactory(factory.django.DjangoModelFactory):
    courier = factory.SubFactory(CourierFactory)
    earnings = factory.Faker('pyfloat')

    class Meta:
        model = DailyEarning


class WeeklyEarningFactory(factory.django.DjangoModelFactory):
    courier = factory.SubFactory(CourierFactory)
    from_date = date.today() - timedelta(days=7)
    to_date = date.today() - timedelta(days=1)
    earnings = 0.0

    class Meta:
        model = WeeklyEarning
