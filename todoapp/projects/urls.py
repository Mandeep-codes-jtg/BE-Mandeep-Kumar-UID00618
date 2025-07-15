from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectMemberApiViewSet 

app_name = 'projects'
router = DefaultRouter()
router.register(r'projects-members', ProjectMemberApiViewSet, basename='project-member')


urlpatterns = [
    path('', include(router.urls)),
]
