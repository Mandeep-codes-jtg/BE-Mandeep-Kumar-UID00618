from rest_framework.viewsets import ModelViewSet
from .models import Todo
from rest_framework import viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import TodoSerializer
from rest_framework.permissions import AllowAny



class TodoPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

class TodoAPIViewSet(ModelViewSet):
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """
    serializer_class = TodoSerializer
    pagination_class = TodoPagination
    permission_classes = [AllowAny]


    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Todo.objects.filter(user_id=user_id).order_by('-date_created')
        return Todo.objects.all().order_by('-date_created')
    
    




