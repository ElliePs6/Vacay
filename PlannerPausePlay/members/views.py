from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  AdminLoginForm,AdminRegistrationForm,RegisterCompanyForm
#from django.contrib.auth.models import User
from VacayVue.models import Company
from django.http import HttpResponse



def admin_landpage(request):
    return render(request, 'authenticate/admin_landpage.html')


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate admin user
            user = authenticate(request, email=email, password=password)
            print(f"Email που λήφθηκε login view: {email}")  # Debugging statement

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
            user.save()
            return redirect('admin_login')  # Redirect to admin login page
        
    else:
        form = AdminRegistrationForm()
    return render(request, 'authenticate/admin_register.html', {'form': form})

def admin_home(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.user.user_type == 'admin':
            companies = Company.objects.all()
            return render(request, 'authenticate/admin_home.html', {'companies': companies})
        else:
            return HttpResponse("You do not have permission to access this page.")
    else:
        return HttpResponse("Please log in to access this page.")


def logout_admin(request):
    logout(request)
    messages.success(request, 'Είσαι Αποσυνδεμένος')
    return redirect('admin_landpage')

def switch_to_company_login(request):
    if request.user.is_authenticated:
        logout(request)  # Log out the user
        return redirect('main_home')   # Redirect to main_home 
    else:
        return redirect('admin_home')  # Redirect to admin login page

def register_company(request):
    if request.method == 'POST':
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            # No need to authenticate and login here, as it's handled by the form's save method
            messages.success(request, 'Registration successful!')
            return redirect('admin_home')  # Assuming 'admin_home' is the correct redirect URL
    else:
        form = RegisterCompanyForm()
    return render(request, 'authenticate/register_company.html', {'form': form})

