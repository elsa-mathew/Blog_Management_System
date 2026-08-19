from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def login_page(request):

    if request.method == "POST":    

        username = request.POST.get('username')
        password = request.POST.get('password')

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user :
            login(request, authenticated_user)
            messages.success(request, 'Login successful!')
            return redirect('home')
    return render(request, 'login.html')

def register_page(request):

    if request.method == "POST":    

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return render(request, 'register.html')

        if email and not email.endswith('@gmail.com'):
            messages.error(request, 'Email must be a valid Gmail address!')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists!')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Registration successful!') 
        return render(request, 'login.html')  
    return render(request, 'register.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

@login_required
def home_page(request):
    return render(request, 'home.html')

@login_required
def logout_view(request):

    if request.method == "POST":

        logout(request)

        messages.success(request, "You have been logged out successfully.")

        return redirect('login')
    return redirect('home')

