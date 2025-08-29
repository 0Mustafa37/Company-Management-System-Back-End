from rest_framework import serializers

from company.models import Department, Project, ProjectEmployee, PerformanceReview


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    def create(self, validated_data):
        company = validated_data["company"]
        department = Department.objects.create(**validated_data)
        company.number_of_departments = company.departments.count()
        company.save()
        return department


class ReadDepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company = serializers.CharField(source="company.name", read_only=True)
    name = serializers.CharField()
    number_of_employees = serializers.IntegerField()
    number_of_projects = serializers.IntegerField()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        company = validated_data["company"]
        department = validated_data["department"]
        project = Project.objects.create(**validated_data)
        company.number_of_projects = company.company_projects.count()
        department.number_of_projects = department.department_projects.count()
        company.save()
        department.save()
        return project


class ReadProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company = serializers.CharField(source="company.name")
    department = serializers.CharField(source="department.name")
    name = serializers.CharField()
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_active = serializers.BooleanField()


class ProjectEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectEmployee
        fields = ["project", "employee"]

    def create(self, validated_data):
        project = validated_data["project"]
        employee = validated_data["employee"]
        assignment = ProjectEmployee.objects.create(**validated_data)
        project.number_of_employees = project.project_employees.count()
        project.save()
        return assignment


class PerformanceReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceReview
        fields = ["employee", "stage", "scheduled_date", "feedback"]


class ReadPerformanceReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    employee = serializers.CharField(source="employee.first_name")
    stage = serializers.CharField()
    scheduled_date = serializers.DateTimeField()
    feedback = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
