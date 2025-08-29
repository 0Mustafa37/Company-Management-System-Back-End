from datetime import date

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel
from user.choices import UserRoles


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email Address"), unique=True)
    role = models.CharField(
        _("Role"), choices=UserRoles.choices, max_length=20, default=UserRoles.EMPLOYEE
    )
    username = models.CharField(_("Username"), max_length=150, unique=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    is_active = models.BooleanField(_("Active"), default=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class Employee(TimeStampedModel):
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="company_employee"
    )
    department = models.ForeignKey(
        "company.Department",
        on_delete=models.CASCADE,
        related_name="department_employee",
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_employee"
    )
    first_name = models.CharField(_("First Name"), max_length=100)
    middle_name = models.CharField(_("Middle Name"), max_length=100, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email Address"), unique=True)
    mobile_number = models.CharField(_("Mobile Number"), max_length=15, blank=True)
    address = models.TextField(_("Address"), blank=True)
    position = models.CharField(_("Position"), max_length=100, blank=True)
    hired_on = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    @property
    def days_employed(self):
        if self.hired_on:
            return (date.today() - self.hired_on).days
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
