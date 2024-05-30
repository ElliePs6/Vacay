from django.shortcuts import render, redirect
from .models import Requests,Employee,Events,CustomUser
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
 

def list_requests(request):
    all_requests=Requests.objects.all()
    return render(request, 'vacayvue/list-requests.html',
        { 'all_requests':all_requests})

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
            # Generate a unique username based on email
            email = form.cleaned_data['email']
            username = email.split('@')[0]  # Example: Use the part before '@' as the username

            # Check if the generated username is unique
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different email.')
                return redirect('register_employee')

            user = form.save(commit=False)
            user.username = username
            user.user_type = 'employee'
            user.join_date = form.cleaned_data['date_joined']

            # Save the user object
            user.save()

            # Check if the employee object is created
            employee, created = Employee.objects.get_or_create(user=user, defaults={'first_name': user.first_name, 'last_name': user.last_name})
            if created:
                messages.success(request, 'Registration successful!')
                return redirect('list-employees')
            else:
                messages.error(request, 'Failed to register employee.')
    else:
        # Assuming the logged-in user is a company
        company = request.user.company  
        initial_data = {'company': company}
        form = RegisterEmployeeForm(initial=initial_data)
    return render(request, 'vacayvue/register_employee.html', {'form': form})
@login_required
def list_employees(request):
    # Filter employees belonging to the currently logged-in company
    company = request.user.company
    employees = Employee.objects.filter(company=company)
    return render(request, 'vacayvue/list-employees.html', {'employees': employees})


def employee_home(request):
    return render(request, 'vacayvue/employee_home.html')


def company_home(request):
    return render(request, 'vacayvue/company_home.html')



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

            # Check if user_type is 'employee' or 'company' and authenticate accordingly
            if user_type == 'employee':
                try:
                    # Retrieve the CustomUser instance associated with the email
                    user = CustomUser.objects.get(email=email, user_type='employee')
                    user = authenticate(request, email=email, password=password)
                except CustomUser.DoesNotExist:
                    user = None
            elif user_type == 'company':
                try:
                    # Retrieve the CustomUser instance associated with the email
                    user = CustomUser.objects.get(email=email, user_type='company')
                    user = authenticate(request, email=email, password=password)
                except CustomUser.DoesNotExist:
                    user = None
            else:
                # Invalid user type
                messages.error(request, 'Invalid user type.')
                return redirect('login')

            # Authenticate the user if found
            if user is not None:
                login(request, user)
                if user.user_type == 'employee':
                    return redirect('employee_home')
                elif user.user_type == 'admin':
                    return redirect ('login')
                elif user.user_type == 'company':
                    return redirect('company_home')
            else:
                # Invalid email or password
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'vacayvue/login.html', {'form': form})

def main_home(request):
    #Get current year   
    current_year=datetime.now().year
    return render(request, 'vacayvue/main_home.html',{       
        'current_year':current_year,
        
    })








