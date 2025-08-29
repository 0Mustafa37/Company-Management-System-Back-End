from django.urls import reverse
from common.tests.base_test import BaseTest
from company.models import Company


class DepartmentAPITestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.department_url = reverse("department-list")
        self.company = Company.objects.create(name="Test Company")
        self.department_data = {"name": "Test Company", "company": self.company.id}

    def test_create_department(self):
        response = self.client.post(
            self.department_url, self.department_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], self.department_data["name"])
        self.assertEqual(response.data["company"], self.department_data["company"])

    def test_create_department_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.department_url, self.department_data, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_departments(self):
        self.client.post(self.department_url, self.department_data, format="json")
        response = self.client.get(self.department_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_department_detail(self):
        create_response = self.client.post(
            self.department_url, self.department_data, format="json"
        )
        department_id = create_response.data["id"]
        detail_url = reverse("department-detail", args=[department_id])
        response = self.client.get(detail_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], department_id)

    def test_update_department(self):
        create_response = self.client.post(
            self.department_url, self.department_data, format="json"
        )
        department_id = create_response.data["id"]
        detail_url = reverse("department-detail", args=[department_id])
        updated_data = {"name": "Updated Department", "company": self.company.id}
        response = self.client.put(detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], updated_data["name"])

    def test_delete_department(self):
        create_response = self.client.post(
            self.department_url, self.department_data, format="json"
        )
        department_id = create_response.data["id"]
        detail_url = reverse("department-detail", args=[department_id])
        response = self.client.delete(detail_url, format="json")
        self.assertEqual(response.status_code, 204)
        get_response = self.client.get(detail_url, format="json")
        self.assertEqual(get_response.status_code, 404)

    def test_create_department_invalid_data(self):
        invalid_data = {"name": "", "company": ""}
        response = self.client.post(self.department_url, invalid_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)
        self.assertIn("company", response.data)

    def test_update_number_of_departments(self):
        initial_count = self.company.number_of_departments
        self.client.post(self.department_url, self.department_data, format="json")
        self.company.refresh_from_db()
        self.assertEqual(self.company.number_of_departments, initial_count + 1)
