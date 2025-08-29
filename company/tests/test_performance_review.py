from django.contrib.auth.hashers import make_password
from django.urls import reverse
from common.tests.base_test import BaseTest
from company.models import Company, Department, Project, PerformanceReview
from user.models import Employee, User


class PerformanceReviewAPITestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.performance_review_url = reverse("performance-review-list")
        self.company = Company.objects.create(name="Test Company")
        self.department = Department.objects.create(
            name="Test Department", company=self.company
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
        self.manager = User.objects.create(
            email="test@manager.com",
            username="test manager",
            password=make_password("TestPass123"),
            role="manager",
        )
        self.admin = User.objects.create(
            email="test@admin.com",
            username="test admin",
            password=make_password("TestPass123"),
            role="admin",
        )

    def test_admin_can_create_review(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "employee": self.employee.id,
            "scheduled_date": "2025-09-01T10:00:00Z",
            "feedback": "Good start",
        }
        response = self.client.post(self.performance_review_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PerformanceReview.objects.count(), 1)

    def test_manager_can_create_review(self):
        self.client.force_authenticate(user=self.manager)
        payload = {
            "employee": self.employee.id,
            "scheduled_date": "2025-09-01T10:00:00Z",
            "feedback": "Promising employee",
        }
        response = self.client.post(self.performance_review_url, payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_employee_cannot_create_review(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "employee": self.employee.id,
            "scheduled_date": "2025-09-01T10:00:00Z",
            "feedback": "Should not work",
        }
        response = self.client.post(self.performance_review_url, payload, format="json")
        self.assertEqual(response.status_code, 403)

    def test_admin_can_change_stage(self):
        self.client.force_authenticate(user=self.admin)
        review = PerformanceReview.objects.create(
            employee=self.employee, scheduled_date="2025-09-01T10:00:00Z", feedback="OK"
        )
        payload = {"stage": "review_scheduled"}
        response = self.client.post(
            reverse("performance-review-change-stage", args=[review.id]),
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.stage, "review_scheduled")

    def test_employee_cannot_change_stage(self):
        self.client.force_authenticate(user=self.user)
        review = PerformanceReview.objects.create(
            employee=self.employee, scheduled_date="2025-09-01T10:00:00Z", feedback="OK"
        )
        payload = {"stage": "review_scheduled"}
        response = self.client.post(
            reverse("performance-review-change-stage", args=[review.id]),
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_can_view_reviews(self):
        self.client.force_authenticate(user=self.manager)
        PerformanceReview.objects.create(
            employee=self.employee, scheduled_date="2025-09-01T10:00:00Z", feedback="OK"
        )
        response = self.client.get(self.performance_review_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
