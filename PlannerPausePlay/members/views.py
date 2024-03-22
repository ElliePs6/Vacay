from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  LoginForm, RegisterCompanyForm,RegisterEmployeeForm
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
    return render(request, 'authenticate/employee_home.html')

def company_home(request):
    return render(request, 'authenticate/company_home.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Είσαι Αποσυνδεμένος')
    return redirect('home')

def register_company(request):
    if request.method == 'POST':
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('admin:index')  # Redirect to the admin index page
    else:
        form = RegisterCompanyForm()
    return render(request, 'authenticate/register_company.html', {'form': form})


def register_employee(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'employee'  # Set user type to 'company'
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('company_home')
    else:
        form = RegisterEmployeeForm()
    return render(request, 'authenticate/register_employee.html', {'form': form})

