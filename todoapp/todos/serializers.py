from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Todo
from users.models import CustomUser as User
from projects.models import Project
from django.db.models import Count, Q


# Add your serializer(s) here

# class TodoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Todo
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class TodoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'user_id', 'name', 'done', 'date_created']
        read_only_fields = ['id', 'date_created']


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        return {
            "todo_id": rep["id"],
            "name": rep["name"],
            "done": rep["done"],
            "date_created": rep["date_created"]
        }

class TodoSerializer1(serializers.ModelSerializer):
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

    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','completed_count','pending_count')

class UserPendingCountSerializer(serializers.ModelSerializer):

    pending_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','pending_count')


class ProjectReportSerializer(serializers.Serializer):
    project_title = serializers.CharField(source='name')
    report = UserWithTodoSerializer(many=True)

    class Meta:
        model = Project
        fields = ('project_title','report')



# class Serializer5(serializers.ModelSerializer):
#     completed_count=serializers.IntegerField(read_only=True)
#     pending_count=serializers.IntegerField(read_only=True)
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email','completed_count','pending_count']

# class projectSerializer(serializers.ModelSerializer):
#     project_title=serializers.CharField(source='name')
#     report=serializers.SerializerMethodField()

#     class Meta:
#         model=Project
#         fields=['project_title','report']

#     def get_report(self,obj):
#         datauser=obj.members.annotate(
#             completed_count=Count('todo', filter=Q(todo__done=True)),
#             pending_count=Count('todo', filter=Q(todo__done=False))
#         )
#         return Serializer5(datauser,many=True).data
    
# class Serializer6(serializers.ModelSerializer):
#     class Meta:
#         model=Project
#         fields=['name','max_members']


class UserProjectStatusSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())