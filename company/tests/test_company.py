from django.urls import reverse
from common.tests.base_test import BaseTest


class CompanyAPITestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.company_url = reverse("company-list")
        self.company_data = {"name": "Test Company"}

    def test_create_company_authenticated(self):
        response = self.client.post(self.company_url, self.company_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], self.company_data["name"])

    def test_create_company_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.company_url, self.company_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_companies(self):
        response = self.client.get(self.company_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_update_company(self):
        create_response = self.client.post(
            self.company_url, self.company_data, format="json"
        )
        self.assertEqual(create_response.status_code, 201)
        company_id = create_response.data["id"]

        update_data = {"name": "Updated Company Name"}
        response = self.client.put(
            reverse("company-detail", args=[company_id]), update_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], update_data["name"])

    def test_delete_company(self):
        create_response = self.client.post(
            self.company_url, self.company_data, format="json"
        )
        self.assertEqual(create_response.status_code, 201)
        company_id = create_response.data["id"]

        response = self.client.delete(
            reverse("company-detail", args=[company_id]), format="json"
        )
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get(
            reverse("company-detail", args=[company_id]), format="json"
        )
        self.assertEqual(get_response.status_code, 404)
