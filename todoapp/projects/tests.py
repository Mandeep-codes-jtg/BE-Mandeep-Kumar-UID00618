from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from projects.models import Project, ProjectMember
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectMemberApiViewSetTestCase (APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@email.com', password='pass')
        self.user2 = User.objects.create_user(email='user2@email.com', password='pass')
        self.user3 = User.objects.create_user(email='user3@email.com', password='pass')

        self.project = Project.objects.create(name='Test Project', max_members=2, status=Project.StatusChoices.TO_BE_STARTED)

        self.add_users_url = reverse('projects:project-member-add-users', kwargs={'pk': self.project.id})
        self.remove_users_url = reverse('projects:project-member-remove-users', kwargs={'pk': self.project.id})
    
    def test_add_users(self):
        response = self.client.post(self.add_users_url, {'user_ids': [self.user1.id, self.user2.id, self.user3.id]}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['logs'][self.user1.id], "Member added Successfully")
        self.assertEqual(response.data['logs'][self.user2.id], "Member added Successfully")
        self.assertEqual(self.project.members.count(), 2)
        self.assertEqual(response.data['logs'][self.user3.id], "Cannot add as project reached max members limit")


    def test_remove_users(self):
        response = self.client.delete(self.remove_users_url, {'user_ids': [self.user1.id, self.user2.id]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['logs'][self.user1.id], "User is not a member of the project")
        self.assertEqual(response.data['logs'][self.user2.id], "User is not a member of the project")
        self.assertEqual(self.project.members.count(), 0)
