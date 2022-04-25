from urllib.robotparser import RequestRate
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm

def logout_user(request):
    logout(request)
    messages.success(request,("You were logged out"))
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("Login Fail. Try again..."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {

    })
    

def register_user(request):
    if request.method =="POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registraction Success!"))
            return redirect('home')
    else: 
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form':form,})