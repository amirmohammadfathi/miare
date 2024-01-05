from django.urls import path
from couriers import views

urlpatterns = [
    path(
        "courier/", views.CreateListCouriers.as_view(),
        name="courier"
    ),
    path(
        "courier/<uuid:pk>/trip/", views.TripOfCourier.as_view(),
        name="trip"
    ),
    path(
        "courier/<uuid:pk>/add/", views.AdditionalEarningOfCourier.as_view(),
        name="additional_earning"
    ),
    path(
        "courier/<uuid:pk>/daily/", views.RetrieveCourierDailyEarning.as_view(),
        name="retrieve_courier_daily_earnings"
    ),
    path(
        "courier/<uuid:pk>/weakly/", views.RetrieveCourierWeeklyEarning.as_view(),
        name="retrieve_courier_weekly_earnings"
    )

]
