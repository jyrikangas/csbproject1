from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from notes.models import Note
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.
def index(request):
    users = User.objects.all() 
    notes = Note.objects.all()
    return render(request, 'index.html', {"users": users, "notes": notes})

def loginView(request):
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return render(request, 'index.html')
        return render(request, 'login.html', {'error': "login fail"})
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get("password")
        User.objects.create_user(username=username, password=password)
        return redirect('/loginView')
    return render(request, 'register.html', {"error": "register failed"})

def add(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'error': "add fail"})
    if request.method == "POST":
        note = request.POST.get('note')
        Note.objects.create(user=request.user, note=note)
    return redirect('/')
        