from rest_framework.test import APIClient
import pytest
from faker import Faker
from movielist.models import Person
from movielist.tests.utils import create_fake_movie
from utils import create_test_cinema


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def set_up():
    for _ in range(5):
        Person.objects.create(name=Faker("pl-PL").name)
    for _ in range(3):
        create_fake_movie()
    create_test_cinema()
