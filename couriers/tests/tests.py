from datetime import timedelta, date

import pytest
from .mixins import BaseTest
from .factories import DailyEarningFactory, TripFactory, AdditionalEarningFactory
from rest_framework import status


@pytest.mark.django_db
class TestCreateListCouriers(BaseTest):
    APP_NAME = "couriers"
    API_URL_NAME = "courier"

    # def test_create_courier(self, django_assert_num_queries, client):
    #     with django_assert_num_queries(1):
    #         data = {'first_name': 'Amir', 'last_name': 'Mohammad'}
    #
    #         res = client.post(self.get_api_url(), json=data, content_type='application/json')
    #         assert res.status_code == status.HTTP_201_CREATED, res.data

    def test_retrieve_all_couriers(self, django_assert_num_queries, courier, client):
        courier_1 = courier
        courier_2 = courier
        courier_3 = courier

        with django_assert_num_queries(1):
            res = client.get(self.get_api_url(), content_type='application/json')
            assert res.status_code == status.HTTP_200_OK, res.data


@pytest.mark.django_db
class TestRetrieveCourierDailyEarning(BaseTest):
    APP_NAME = "couriers"
    API_URL_NAME = "retrieve_courier_daily_earnings"

    def test_witness_sign_before_owners_and_tenant_sign(self, client, django_assert_num_queries, courier):
        courier_1 = courier
        TripFactory.create(courier=courier_1, income=555000)
        AdditionalEarningFactory.create(courier=courier_1, amount=555000, is_for_award=True)
        AdditionalEarningFactory.create(courier=courier_1, amount=8000, is_for_award=False)

        with django_assert_num_queries(1):
            res = client.get(self.get_api_url({"pk": courier_1.id}), content_type='application/json')
            assert res.status_code == status.HTTP_200_OK, res


#
#
@pytest.mark.django_db
class TestRetrieveCourierWeeklyEarning(BaseTest):
    APP_NAME = "couriers"
    API_URL_NAME = "retrieve_courier_weekly_earnings"

    def test_witness_sign_before_owners_and_tenant_sign(self, client, django_assert_num_queries, courier):
        courier_1 = courier
        TripFactory.create(courier=courier_1, income=555000)
        AdditionalEarningFactory.create(courier=courier_1, amount=555000, is_for_award=True)
        AdditionalEarningFactory.create(courier=courier_1, amount=8000, is_for_award=False)
        for i in range(6):
            DailyEarningFactory.create(courier=courier_1, date=date.today() - timedelta(days=i))

        with django_assert_num_queries(1):
            res = client.get(self.get_api_url({"pk": courier_1.id}), content_type='application/json')
            assert res.status_code == status.HTTP_200_OK, res
