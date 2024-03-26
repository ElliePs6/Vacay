from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  LoginForm, RegisterCompanyForm,RegisterEmployeeForm,AdminLoginForm,AdminRegistrationForm
#from django.contrib.auth.models import User
from VacayVue.models import Companies,Employees
from django.http import HttpResponse
from VacayVue.views import home
from django.contrib.auth.decorators import login_required



def first_home(request):
    return render(request, 'authenticate/first_home.html')

def admin_home(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.user.user_type == 'admin':
            related_companies = Companies.objects.all()
            return render(request, 'authenticate/admin_home.html', {'related_companies': related_companies})
        else:
            return HttpResponse("You do not have permission to access this page.")
    else:
        return HttpResponse("Please log in to access this page.")

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate admin user
            user = authenticate(request, email=email, password=password)
            print(f"Email received in login view: {email}")  # Debugging statement

            if user is not None:
                print(f'User authenticated: {user}')
                print(f'User type: {user.user_type}')
                login(request, user)
                if user.user_type == 'admin':
                    return redirect('admin_home')  # Redirect to admin dashboard
            else:
                print('Authentication failed')  # Debugging statement
                # Incorrect credentials
                messages.error(request, 'Incorrect email or password.')
                return redirect('admin_login')
    else:
        form = AdminLoginForm()
    return render(request, 'authenticate/admin_login.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'admin' 
            user.save()
            return redirect('admin_login')  # Redirect to admin login page
    else:
        form = AdminRegistrationForm()
    return render(request, 'authenticate/admin_register.html', {'form': form})

def logout_admin(request):
    logout(request)
    messages.success(request, 'Είσαι Αποσυνδεμένος')
    return redirect('first_home')

def switch_to_company_login(request):
    if request.user.is_authenticated:
        logout(request)  # Log out the user
        return redirect('home')  # Redirect to company login page
    else:
        return redirect('admin_home')  # Redirect to admin login page

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

def logout_user(request):
    logout(request)
    messages.success(request, 'Είσαι Αποσυνδεμένος')
    return redirect('home')

def employee_home(request):
    return render(request, 'authenticate/employee_home.html')

def company_home(request):
    return render(request, 'authenticate/company_home.html')


def register_company(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'company' 
            user.companyname = form.cleaned_data['companyname']  # Assign companyname from form
            user.hrname = form.cleaned_data['hrname']  # Assign hrname from form
            user.save()
            messages.success(request, 'Company registration successful!')
            return redirect('admin_home')  # Redirect to admin home page
        else:
            print(form.errors)
    else:
        form = RegisterCompanyForm()
    return render(request, 'authenticate/register_company.html', {'form': form})

@login_required
def register_employee(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'employee'
            user.join_date = form.cleaned_data['date_joined']  # Assign companyname from form
            user.username = form.cleaned_data['username']
            user.save()

            messages.success(request, 'Registration successful!')
            return redirect('company_home')
    else:
        form = RegisterEmployeeForm()
    return render(request, 'authenticate/register_employee.html', {'form': form})

    