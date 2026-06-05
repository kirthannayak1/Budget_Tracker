from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User


# REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        is_daily_waged = request.POST['is_daily_waged'] == "True"
        salary = 0

        if not is_daily_waged:
            salary = request.POST.get('salary', 0)

        # Password match check
        if password1 != password2:
            return render(request, 'accounts/register.html', {
                "error": "Passwords do not match"
            })

        # Create user
        user = User.objects.create_user(
    username=username,
    email=email,
    password=password1,
    is_daily_waged=is_daily_waged,
    monthly_salary=salary
)

        login(request, user)
        return redirect('dashboard')  # comes from finance app now

    return render(request, 'accounts/register.html')


# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')  # finance dashboard
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')