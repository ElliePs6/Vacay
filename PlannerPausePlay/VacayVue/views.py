from django.shortcuts import render, redirect
from .models import Requests,Employees,Events
from .forms import RequestForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import  LoginForm,RegisterEmployeeForm




def employee_navbar(request):
    return render(request, 'vacayvue/employee_navbar.html')

def company_navbar(request):
    return render(request, 'vacayvue/company_navbar.html')

def calendar(request):  
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'vacayvue/calendar.html',context)
 
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name, 
            'id':event.id,                                                                                                                                                                                      
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)
 
def list_employees(request):
    employees=Employees.objects.all()
    return render(request, 'vacayvue/list-employees.html',
        { 'employees':employees})

def add_request(request):
    submitted = False
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the same view with the 'submitted' parameter in the URL
            return redirect('/add-request/?submitted=True')
    else:
        form = RequestForm()

    # Check if the 'submitted' parameter is present in the URL
    if 'submitted' in request.GET and request.GET['submitted'] == 'True':
        submitted = True

    return render(request, 'vacayvue/add-request.html', {'form': form, 'submitted': submitted})

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

def employee_home(request):
    return render(request, 'vacayvu/employee_home.html')

def company_home(request):
    return render(request, 'vacayvue/company_home.html')

def list_requests(request):
    all_requests=Requests.objects.all()
    return render(request, 'vacayvue/list-requests.html',
        { 'all_requests':all_requests})


def logout_user(request):
    logout(request)
    messages.success(request, 'Είσαι Αποσυνδεμένος')
    return redirect('main_home')

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

def main_home(request):
    #Get current year   
    current_year=datetime.now().year
    return render(request, 'vacayvue/main_home.html',{       
        'current_year':current_year,
        
    })








