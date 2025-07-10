from rest_framework.viewsets import ModelViewSet
from .models import Todo
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated


class TodoPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

class TodoAPIViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    pagination_class = TodoPagination
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-date_created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to edit this todo.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to delete this todo.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    




