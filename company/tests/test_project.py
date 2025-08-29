from django.contrib.auth.hashers import make_password
from django.urls import reverse
from common.tests.base_test import BaseTest
from company.models import Company, Department, Project
from user.models import Employee, User


class ProjectAPITestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.project_url = reverse("project-list")
        self.company = Company.objects.create(name="Test Company")
        self.department = Department.objects.create(
            name="Test Department", company=self.company
        )
        self.project_data = {
            "name": "Test Project",
            "description": "A test project",
            "start_date": "2025-09-01",
            "end_date": "2025-10-05",
            "is_active": True,
            "company": self.company.id,
            "department": self.department.id,
        }

    def test_create_project(self):
        response = self.client.post(self.project_url, self.project_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], self.project_data["name"])
        self.assertEqual(response.data["company"], self.project_data["company"])
        self.assertEqual(response.data["department"], self.project_data["department"])

    def test_create_project_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.project_url, self.project_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_projects(self):
        self.client.post(self.project_url, self.project_data, format="json")
        response = self.client.get(self.project_url, format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_project_detail(self):
        create_response = self.client.post(
            self.project_url, self.project_data, format="json"
        )
        project_id = create_response.data["id"]
        detail_url = reverse("project-detail", args=[project_id])
        response = self.client.get(detail_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], project_id)

    def test_update_project(self):
        create_response = self.client.post(
            self.project_url, self.project_data, format="json"
        )
        project_id = create_response.data["id"]
        detail_url = reverse("project-detail", args=[project_id])
        updated_data = {
            "name": "Updated Project",
            "description": "An updated test project",
            "start_date": "2025-10-01",
            "end_date": "2025-10-31",
            "is_active": False,
            "company": self.company.id,
            "department": self.department.id,
        }
        response = self.client.put(detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], updated_data["name"])

    def test_delete_project(self):
        create_response = self.client.post(
            self.project_url, self.project_data, format="json"
        )
        project_id = create_response.data["id"]
        detail_url = reverse("project-detail", args=[project_id])
        response = self.client.delete(detail_url, format="json")
        self.assertEqual(response.status_code, 204)
        get_response = self.client.get(detail_url, format="json")
        self.assertEqual(get_response.status_code, 404)

    def test_create_project_invalid_data(self):
        invalid_data = {
            "name": "",
            "description": "",
            "start_date": "invalid-date",
            "end_date": "invalid-date",
            "is_active": "not-a-boolean",
            "company": "",
            "department": "",
        }
        response = self.client.post(self.project_url, invalid_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_number_of_projects_on_create(self):
        initial_company_projects = self.company.number_of_projects
        initial_department_projects = self.department.number_of_projects

        self.client.post(self.project_url, self.project_data, format="json")

        self.company.refresh_from_db()
        self.department.refresh_from_db()

        self.assertEqual(self.company.number_of_projects, initial_company_projects + 1)
        self.assertEqual(
            self.department.number_of_projects, initial_department_projects + 1
        )


class ProjectEmployeeAPITestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.manager = User.objects.create(
            email="test@manager.com",
            username="test manager",
            password=make_password("TestPass123"),
            role="manager",
        )
        self.client.force_authenticate(user=self.manager)
        self.project_employee_url = reverse("project-assign-employee")
        self.company = Company.objects.create(name="Test Company")
        self.department = Department.objects.create(
            name="Test Department", company=self.company
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="A test project",
            start_date="2025-09-01",
            end_date="2025-10-05",
            is_active=True,
            company=self.company,
            department=self.department,
        )
        self.employee = Employee.objects.create(
            first_name="test",
            last_name="Employee",
            email="test@Employee.com",
            user=self.user,
            company=self.company,
            department=self.department,
            position="Developer",
        )

    def test_assign_employee_to_project(self):
        data = {"project": self.project.id, "employee": self.employee.id}
        response = self.client.post(self.project_employee_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["project"], data["project"])
        self.assertEqual(response.data["employee"], data["employee"])

    def test_assign_employee_to_project_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {"project": self.project.id, "employee": self.employee.id}
        response = self.client.post(self.project_employee_url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_assign_employee_to_project_invalid_data(self):
        invalid_data = {"project": "", "employee": ""}
        response = self.client.post(
            self.project_employee_url, invalid_data, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_update_number_of_employees_on_assignment(self):
        initial_project_employees = self.project.project_employees.count()
        data = {"project": self.project.id, "employee": self.employee.id}
        self.client.post(self.project_employee_url, data, format="json")
        self.project.refresh_from_db()
        self.assertEqual(
            self.project.project_employees.count(), initial_project_employees + 1
        )

    def test_assign_same_employee_to_project_multiple_times(self):
        data = {"project": self.project.id, "employee": self.employee.id}
        response1 = self.client.post(self.project_employee_url, data, format="json")
        response2 = self.client.post(self.project_employee_url, data, format="json")
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)

    def test_assign_employee_with_role_user(self):
        self.client.force_authenticate(user=self.user)
        data = {"project": self.project.id, "employee": self.employee.id}
        response = self.client.post(self.project_employee_url, data, format="json")
        self.assertEqual(response.status_code, 403)
