from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Project, ProjectMember
from rest_framework.permissions import AllowAny
User = get_user_model()

class ProjectMemberApiViewSet(viewsets.ViewSet):
    """
    ViewSet to add/remove members to/from a project with constraints:
    - A user can be a member of max 2 projects.
    - A project can have max N members (max_members field).
    - Users can be added or removed by providing list of user_ids in request body.
    """
    permission_classes = [AllowAny]

    def get_project(self, pk):
        return get_object_or_404(Project, pk=pk)

    @action(detail=True, methods=['post'], url_path='add-users')
    def add_users(self, request, pk=None):
        project = self.get_project(pk)
        user_ids = request.data.get("user_ids", [])
        logs = {}

        if project.status == Project.StatusChoices.COMPLETED:
            for uid in user_ids:
                logs[uid] = "Cannot add members to a completed project"
            return Response({"logs": logs}, status=status.HTTP_400_BAD_REQUEST)

        current_member_count = project.members.count()
        max_members = project.max_members

        existing_member_ids = set(project.members.values_list("id", flat=True))

        user_projects_count = dict(
            User.objects.filter(id__in=user_ids)
            .annotate(project_count=Count('project_working_on'))
            .values_list('id', 'project_count')
        )

        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                logs[user_id] = "User does not exist"
                continue

            if user_id in existing_member_ids:
                logs[user_id] = "User is already a Member"
                continue

            if user_projects_count.get(user_id, 0) >= 2:
                logs[user_id] = "Cannot add as User is a member in two projects"
                continue

            if current_member_count >= max_members:
                logs[user_id] = "Cannot add as project reached max members limit"
                continue

            ProjectMember.objects.create(project=project, member=user)
            logs[user_id] = "Member added Successfully"
            current_member_count += 1
            user_projects_count[user_id] = user_projects_count.get(user_id, 0) + 1
            existing_member_ids.add(user_id)

        return Response({"logs": logs})

    @action(detail=True, methods=['delete'], url_path='remove-users')
    def remove_users(self, request, pk=None):
        project = self.get_project(pk)
        user_ids = request.data.get("user_ids", [])
        logs = {}

        if project.status == Project.StatusChoices.COMPLETED:
            for uid in user_ids:
                logs[uid] = "Cannot remove members from a completed project"
            return Response({"logs": logs}, status=status.HTTP_400_BAD_REQUEST)

        existing_member_ids = set(project.members.values_list("id", flat=True))

        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                logs[user_id] = "User does not exist"
                continue

            if user_id not in existing_member_ids:
                logs[user_id] = "User is not a member of the project"
                continue

            ProjectMember.objects.filter(project=project, member=user).delete()
            logs[user_id] = "Member removed Successfully"
            existing_member_ids.remove(user_id)

        return Response({"logs": logs})




"""
       constraints
        - a user can be a member of max 2 projects only
        - a project can have at max N members defined in database for each project
       functionalities
       - add users to projects

         Request
         { user_ids: [1,2,...n] }
         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }
         following are the possible status messages
         case1: if user is added successfully then - "Member added Successfully"
         case2: if user is already a member then - "User is already a Member"
         case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

         there will be many other cases think of that

       - update to remove users from projects

         Request
         { user_ids: [1,2,...n] }

         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }

         there will be many other cases think of that and share on forum
    """
    