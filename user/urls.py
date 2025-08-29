from django.urls import path
from rest_framework.routers import DefaultRouter

from user.apis import LoginAPIView, RegisterAPI, EmployeeAPIView

router = DefaultRouter()
router.register("employee", EmployeeAPIView, basename="employee")
urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPI.as_view(), name="register"),
]
urlpatterns += router.urls
