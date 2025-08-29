from django.contrib.auth.hashers import make_password
from django.urls import reverse
from common.tests.base_test import BaseTest
from company.models import Company, Department
from user.models import User


class EmployeeAPITestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.manager = User.objects.create(
            email="test@manager.com",
            username="test manager",
            password=make_password("TestPass123"),
            role="manager",
        )
        self.client.force_authenticate(user=self.manager)
        self.employee_url = reverse("employee-list")
        self.company = Company.objects.create(name="Test Company")
        self.department = Department.objects.create(
            name="Test Department", company=self.company
        )
        self.employee_data = {
            "first_name": "test",
            "middle_name": "A",
            "last_name": "employee",
            "email": "test@employee.com",
            "mobile_phone": "1234567890",
            "address": "123 Test St",
            "position": "Developer",
            "company": self.company.id,
            "department": self.department.id,
            "user": self.user.id,
        }

    def test_create_employee(self):

        response = self.client.post(
            self.employee_url, self.employee_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["first_name"], self.employee_data["first_name"])
        self.assertEqual(response.data["last_name"], self.employee_data["last_name"])
        self.assertEqual(response.data["email"], self.employee_data["email"])
        self.assertEqual(response.data["company"], self.employee_data["company"])
        self.assertEqual(response.data["department"], self.employee_data["department"])

    def test_create_employee_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.employee_url, self.employee_data, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_employees(self):
        self.client.post(self.employee_url, self.employee_data, format="json")
        response = self.client.get(self.employee_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_employee_detail(self):
        create_response = self.client.post(
            self.employee_url, self.employee_data, format="json"
        )
        employee_id = create_response.data["id"]
        detail_url = reverse("employee-detail", args=[employee_id])
        response = self.client.get(detail_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], employee_id)

    def test_update_employee(self):
        create_response = self.client.post(
            self.employee_url, self.employee_data, format="json"
        )
        employee_id = create_response.data["id"]
        detail_url = reverse("employee-detail", args=[employee_id])
        updated_data = {
            "first_name": "updated",
            "middle_name": "B",
            "last_name": "employee",
            "email": "test@manager.com",
            "address": "456 Updated St",
            "position": "Manager",
            "company": self.company.id,
            "department": self.department.id,
        }
        response = self.client.patch(detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], updated_data["first_name"])
        self.assertEqual(response.data["position"], updated_data["position"])

    def test_delete_employee(self):
        create_response = self.client.post(
            self.employee_url, self.employee_data, format="json"
        )
        employee_id = create_response.data["id"]
        detail_url = reverse("employee-detail", args=[employee_id])
        response = self.client.delete(detail_url, format="json")
        self.assertEqual(response.status_code, 204)
        get_response = self.client.get(detail_url, format="json")
        self.assertEqual(get_response.status_code, 404)

    def test_create_employee_invalid_data(self):
        invalid_data = {
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "email": "invalidemail",
            "mobile_phone": "",
            "address": "",
            "position": "",
            "company": "",
            "department": "",
        }
        response = self.client.post(self.employee_url, invalid_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_number_of_employees(self):
        initial_count = self.department.number_of_employees
        self.client.post(self.employee_url, self.employee_data, format="json")
        updated_count = Department.objects.get(
            id=self.department.id
        ).number_of_employees
        self.assertEqual(updated_count, initial_count + 1)

    def test_update_number_of_employees_company(self):
        initial_count = self.company.number_of_employees
        self.client.post(self.employee_url, self.employee_data, format="json")
        updated_count = Company.objects.get(id=self.company.id).number_of_employees
        self.assertEqual(updated_count, initial_count + 1)

    def test_wrong_role_create_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.employee_url, self.employee_data, format="json"
        )
        self.assertEqual(response.status_code, 403)
