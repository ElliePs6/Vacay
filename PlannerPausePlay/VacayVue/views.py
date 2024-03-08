from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Requests


def all_requests(request):
    list_requests=Requests.objects.all()
    return render(request, 'vacayvue/list-requests.html',
        { 'list_requests':list_requests})


def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    month=month.capitalize()
    #convert month from name to number
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)

    #create a callendar
    cal=HTMLCalendar().formatmonth(year,month_number)
    now=datetime.now()
    #Get current year   
    current_year=now.year
    #Get current time
    time=now.strftime('%I:%M %p')
    
    return render(request, 'vacayvue/home.html',{
        'year':year,
        'month':month,
        'month_number':month_number,
        'cal':cal,
        'current_year':current_year,
        'time':time 
    })


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                # Set user as staff (not sure if this is intended)
                user.is_staff = True
                user.save()
                return redirect('login_user')
        else:
            messages.error(request, "Passwords don't match")
            return redirect('register')
    else:
        # Handle GET request or other methods if needed
        return render(request, 'vacayvue/register.html')

    

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f'Successfully authenticated user: {user.username}')
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid login credentials.')
    else:
        form = LoginForm()

    return render(request, 'vacayvue/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')




'''
def my_view(request):
    if request.user.is_authenticated:
        # User is authenticated, perform your actions here
        return render(request, 'home.html')
    else:
        # User is not authenticated, you might want to redirect them to a login page
        return HttpResponseForbidden("You are not allowed to access this page. Please log in.")
        '''
