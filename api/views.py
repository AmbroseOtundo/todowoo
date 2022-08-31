import imp
from rest_framework import generics, permissions
from .serializers import TodoSerializer
from todo.models import Todo

# A class based view that inherits from the ListAPIView class. It is used to list all the todos that
# are completed.
class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        Todo.objects.filter(user=user, datecompleted_isnull=False)
