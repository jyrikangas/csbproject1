from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from notes.models import Note
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    users = User.objects.all() 
    notes = Note.objects.all()
    user = request.user
    return render(request, 'index.html', {"users": users, "notes": notes, "user": user})

def loginView(request):
    if request.method == "POST":
        ## if tries > 3, return error
        username =request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect('/')
        return render(request, 'login.html', {'error': "login fail"})
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get("password")
        ##call a function to check password strength, if not strong enough, return error
        ##if not check_password_strength(password):
        ##    return render(request, 'register.html', {"error": "password not strong enough"})
        
        User.objects.create_user(username=username, password=password)
        return redirect('/loginView')
    return render(request, 'register.html', {"error": "register failed"})

def check_password_strength(password):
    # Check if password is at least 8 characters long
    if len(password) < 8:
        return False

    # Check if password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if password contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check if password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check if password contains at least one special character
    special_chars = "!@#$%^&*()-+"
    if not any(char in special_chars for char in password):
        return False

    return True

##login_required
def add(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'error': "add fail"})
    if request.method == "POST":
        note = request.POST.get('note')
        Note.objects.create(user=request.user, note=note)
        print(request.user)
        print(note)
        print(Note.objects.get(note=note))
    return redirect('/')

def logoutView(request):
    logout(request)
    return redirect('/')

##login_required
def accountView(request, username):
    ##   if not request.user.is_authenticated:
    ##   return render(request, 'login.html', {'error': "add fail"})
    pageowner = User.objects.get(username=username)
    notes = Note.objects.filter(user=pageowner)
    user=request.user
    return render(request, 'account.html', {"notes": notes, "user": user, "pageowner": pageowner})

##login_required
def deleteView(request, id):
    ##   if not request.user.is_authenticated:
    ##   return render(request, 'login.html', {'error': "add fail"})
    note = Note.objects.get(id=id)
    username=note.user.username
    note.delete()
    return redirect('/accounts/'+username)