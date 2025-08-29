from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from company.models import Department, Project, ProjectEmployee, PerformanceReview
from company.serializers import (
    DepartmentSerializer,
    ReadDepartmentSerializer,
    ProjectSerializer,
    ReadProjectSerializer,
    ProjectEmployeeSerializer,
    PerformanceReviewSerializer,
    ReadPerformanceReviewSerializer,
)
from user.permission import IsAdminOrManager, IsAdmin


class DepartmentAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return self.queryset.select_related("company").all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadDepartmentSerializer
        return DepartmentSerializer


class ProjectAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.queryset.select_related("company", "department").all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadProjectSerializer
        return ProjectSerializer


class AssignProjectToEmployeeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    queryset = ProjectEmployee.objects.all()
    serializer_class = ProjectEmployeeSerializer


class PerformanceReviewAPIView(ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "employee":
            return self.queryset.filter(employee__email=user.email)
        return self.queryset

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAdminOrManager()]
        elif self.action in ["update", "partial_update", "change_stage"]:
            return [IsAdminOrManager()]
        elif self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadPerformanceReviewSerializer
        return PerformanceReviewSerializer

    @action(detail=True, methods=["post"], url_path="change-stage")
    def change_stage(self, request, pk=None):
        review = self.get_object()
        new_stage = request.data.get("stage")

        if not new_stage:
            return Response({"error": "stage field is required"}, status=400)

        if review.update_stage(new_stage):
            return Response({"status": f"Stage updated to {new_stage}"}, status=200)
        return Response(
            {"error": f"Invalid transition from {review.stage} to {new_stage}"},
            status=400,
        )
