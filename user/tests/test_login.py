from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import User


class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user_data = {
            "email": "test@user.com",
            "password": "TestPass123",
            "username": "test user",
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["message"], "User registered successfully")
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        User.objects.create(
            email=self.user_data["email"],
            password=make_password(self.user_data["password"]),
            username=self.user_data["username"],
        )
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        self.client.post(self.register_url, self.user_data, format="json")
        login_data = {"email": self.user_data["email"], "password": "WrongPass123"}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_login_with_missing_fields(self):
        login_data = {"email": self.user_data["email"]}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, 400)
