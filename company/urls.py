from django.urls import path
from rest_framework.routers import DefaultRouter

from company.apis import (
    CompanyAPIView,
    DepartmentAPIView,
    ProjectAPIView,
    AssignProjectToEmployeeAPIView,
    PerformanceReviewAPIView,
)

router = DefaultRouter()
router.register("company", CompanyAPIView, basename="company")
router.register("department", DepartmentAPIView, basename="department")

router.register("project", ProjectAPIView, basename="project")
router.register(
    r"performance-reviews", PerformanceReviewAPIView, basename="performance-review"
)
urlpatterns = [
    path(
        "project-assign-employee/",
        AssignProjectToEmployeeAPIView.as_view(),
        name="project-assign-employee",
    ),
]
urlpatterns += router.urls
