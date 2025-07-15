from django.urls import include, path
from django.contrib import admin

api_urls = [
    path('todos/', include('todos.urls')),
    path('', include('users.urls', namespace='users')),
    path('', include('projects.urls', namespace='projects'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))
]

