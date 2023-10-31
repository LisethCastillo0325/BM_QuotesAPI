import pytest
from faker import Faker

from django.conf import settings
from django.core.management import call_command
from django.contrib.auth.models import User
from django_api.test.providers.user_providers import EmailProvider


fake = Faker()
fake.add_provider(EmailProvider)


@pytest.fixture
def user_creation():
    return User(
        email=fake.custom_email(), 
        password=fake.phone_number(),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
