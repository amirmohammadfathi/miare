from rest_framework.test import APIClient

import pytest
from couriers.tests.factories import *


@pytest.fixture
def courier() -> Courier:
    return CourierFactory.create()


@pytest.fixture
def client() -> APIClient:
    return APIClient()

