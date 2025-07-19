from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project
from users.models import CustomUser as User
from todos.models import Todo


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for basic user details
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class TodoSerializer1(serializers.ModelSerializer):
    """
    Serializer for Todo updated according to request-response format
    """
    creator = UserSerializer(source='user')  # map 'user' FK to 'creator'

    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ('id', 'name', 'status', 'created_at', 'creator')

    def get_status(self, obj):
        return 'Done' if obj.done else 'To Do'  # assuming status is a boolean

    def get_created_at(self, obj):
        return obj.date_created.strftime('%-I:%M %p, %d %b, %Y')


class UserWithTodoSerializer(serializers.ModelSerializer):
    """
    Serializer for all user details including their
    completed_count and pending_count for users.
    """

    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','completed_count','pending_count')


class UserPendingCountSerializer(serializers.ModelSerializer):
    """
    Serializer for all user details including their pending todo counts.
    """

    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','pending_count')


class ProjectReportSerializer(serializers.Serializer):
    """
    Serializer for Projects including data of all members project-wise
    """
    project_title = serializers.CharField(source='name')
    report = UserWithTodoSerializer(many=True)

    class Meta:
        model = Project
        fields = ('project_title','report')


class UserProjectStatusSerializer(serializers.Serializer):
    """
    Serializer for user details including all their projects with status.
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())
