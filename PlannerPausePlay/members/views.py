from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  LoginForm, RegisterUserForm
#from django.contrib.auth.models import User

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                print(f'User authenticated: {user}')
                print(f'User type: {user.user_type}')
                login(request, user)
                if user.user_type == 'employee':
                    print('Redirecting to employee_home')
                    return redirect('employee_home')
                elif user.user_type == 'company':
                    print('Redirecting to company_home')
                    return redirect('company_home')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'authenticate/login.html', {'form': form})


def employee_home(request):
    return render(request, 'authenticate/login_employee.html')

def company_home(request):
    return render(request, 'authenticate/login_company.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Είσαι Αποσυνδεμένος')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'company'  # Set user type to 'company'
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form})

def user_view(request):
    return render(request, 'authenticate/user_view.html')