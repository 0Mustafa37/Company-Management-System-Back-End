from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel
from company.choices import Stages


# Create your models here.


class Company(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    number_of_employees = models.IntegerField(_("Number of employees"), default=0)
    number_of_departments = models.IntegerField(_("Number of departments"), default=0)
    number_of_projects = models.IntegerField(_("Number of projects"), default=0)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


class Department(TimeStampedModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(_("Name"), max_length=255)
    number_of_employees = models.IntegerField(_("Number of employees"), default=0)
    number_of_projects = models.IntegerField(_("Number of projects"), default=0)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class Project(TimeStampedModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_projects"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department_projects",
        null=True,
        blank=True,
    )
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class ProjectEmployee(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_employees"
    )
    employee = models.ForeignKey(
        "user.Employee", on_delete=models.CASCADE, related_name="employee_projects"
    )
    assigned_at = models.DateTimeField(_("Assigned At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Project Employee")
        verbose_name_plural = _("Project Employees")
        unique_together = ("project", "employee")


class PerformanceReview(TimeStampedModel):
    employee = models.ForeignKey(
        "user.Employee",
        on_delete=models.CASCADE,
        related_name="performance_reviews_employee",
    )
    stage = models.CharField(
        max_length=20, choices=Stages.choices, default=Stages.PENDING_REVIEW
    )
    scheduled_date = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Performance Review")
        verbose_name_plural = _("Performance Reviews")
        ordering = ["-created_at"]

    def can_transition(self, new_stage):
        allowed_transitions = {
            Stages.PENDING_REVIEW: [Stages.REVIEW_SCHEDULED],
            Stages.REVIEW_SCHEDULED: [Stages.FEEDBACK_PROVIDED],
            Stages.FEEDBACK_PROVIDED: [Stages.UNDER_APPROVAL],
            Stages.UNDER_APPROVAL: [Stages.REVIEW_APPROVED, Stages.REVIEW_REJECTED],
            Stages.REVIEW_REJECTED: [Stages.FEEDBACK_PROVIDED],
        }
        return new_stage in allowed_transitions.get(self.stage, [])

    def update_stage(self, new_stage):
        if self.can_transition(new_stage):
            self.stage = new_stage
            self.save()
            return True
        return False
