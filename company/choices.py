from django.db import models


class Stages(models.TextChoices):
    PENDING_REVIEW = "pending_review", "Pending Review"
    REVIEW_SCHEDULED = "review_scheduled", "Review Scheduled"
    FEEDBACK_PROVIDED = "feedback_provided", "Feedback Provided"
    UNDER_APPROVAL = "under_approval", "Under Approval"
    REVIEW_APPROVED = "review_approved", "Review Approved"
    REVIEW_REJECTED = "review_rejected", "Review Rejected"
