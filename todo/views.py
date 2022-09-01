from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        # match password
        if request.POST['password1'] == request.POST['password2']:
        # create a new user
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'] )
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username is already taken, please choose another one'})
 
        else:
            # tell user pass did not match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords do not match'})

@login_required   
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        # match password
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required 
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            # create and dont put any data
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad Data Pased In'})


@login_required 
def currenttodos(request):
    # show the todos
    todos = Todo.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required 
def completedtodos(request):
    # show the todos
    todos = Todo.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required 
def viewtodo(request, todo_pk):
    # show the todos
    # the user=request.user makes sure the todos are salient to only the owner
    todo = get_object_or_404(Todo, pk=todo_pk,  user=request.user)
   

    # This is a function that is called when the user clicks on the todo item. It will show the todo
    # item and allow the user to edit it.
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error': 'Bad info'})

@login_required 
def completetodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required 
def deletetodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

