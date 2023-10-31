import pytest

from faker import Faker

from django_api.test.providers.user_providers import EmailProvider

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


fake = Faker()
fake.add_provider(EmailProvider)

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_super_user_create(user_creation):
    user_creation.is_superuser = True
    user_creation.save()
    assert user_creation.is_superuser

def test_user_creaction_fail():
    with pytest.raises(Exception):
        User.objects.create(
             email='user@gmail.com'
        )

class TestUpdateUserViewSet(APITestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
        )
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = "admin@example.com"
        password = "admin123"
        username = "Test User"
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name="Admin",
            last_name="User",
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
