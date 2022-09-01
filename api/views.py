from lib2to3.pgen2 import token
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.utils import timezone
from rest_framework import generics, permissions
from .serializers import TodoSerializer,TodoCompleteSerializer
from todo.models import Todo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

# api signup auth
"""
    If the request method is POST, then create a user with the username and password provided in the
    request body, and return a JsonResponse with a token.
"""
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password = data['password'] )
            user.save()
           # Creating a token for the user and returning it in the response.
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status = 201)
        except IntegrityError:
            return  JsonResponse({'error':'That username is already taken, please choose another one'}, status = 400)

# login token
@csrf_exempt
def login(request):
    if request.method == 'POST':
            data = JSONParser().parse(request)
            user = authenticate(request, username=data['username'], password=data['password'])
            
            # Creating a token for the user.
            if user is None:
                return  JsonResponse({'error':'Could not login. Please check username and password'}, status = 400)
            else:
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)
                return JsonResponse({'token':str(token)}, status = 201)

# A class based view that inherits from the ListAPIView class. It is used to list all the todos that
# are completed.
class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return all Todo objects that have a user that matches the current user, and have a datecompleted
        that is not null, and order them by the datecompleted in descending order.
        :return: A list of completed todos
        """
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')

# todo api create
class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve update and destroy
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # complete todo
class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        """
        When the user updates the status of a task, the datecompleted field will be updated with the
        current time.
        
        :param serializer: The serializer instance that should be saved
        """
    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()