from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from user.models import User


class BaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@user.com",
            username="test user",
            password=make_password("TestPass123"),
        )
        self.client.force_authenticate(user=self.user)
