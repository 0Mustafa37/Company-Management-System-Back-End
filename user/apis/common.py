from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.models import Employee
from user.permission import IsAdminOrManager
from user.serializers import EmployeeSerializer, ReadEmployeeSerializer


class EmployeeAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return self.queryset.select_related("company", "department").all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadEmployeeSerializer
        return EmployeeSerializer
