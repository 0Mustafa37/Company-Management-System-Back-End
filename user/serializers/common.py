from rest_framework import serializers

from company.models import Department, Project
from user.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        company = validated_data["company"]
        department = validated_data["department"]
        employee = Employee.objects.create(**validated_data)
        company.number_of_employees = company.company_employee.count()
        department.number_of_employees = department.department_employee.count()
        company.save()
        department.save()
        return employee


class ReadEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    company = serializers.CharField(source="company.name")
    department = serializers.CharField(source="department.name")
    email = serializers.CharField()
    mobile_number = serializers.CharField()
    address = serializers.CharField()
    position = serializers.CharField()
    days_employed = serializers.IntegerField()
