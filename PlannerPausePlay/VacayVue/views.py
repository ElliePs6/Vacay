from django.shortcuts import render, redirect
from .models import Requests,Employee,Events,CustomUser,Company
from .forms import RequestForm,LoginForm,RegisterEmployeeForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404




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
    
    print("Received request to add event:")
    print("Title:", title)
    print("Start:", start)
    print("End:", end)
    
    event = Events(name=str(title), start=start, end=end)
    event.save()
    
    print("Event saved successfully:", event)
    
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



def register_employee(request):
    print("etrekse to register employee")
    if request.method == 'POST':
        print(request.POST)  # Print form data
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            print(f"Logged-in user: {request.user}")  # Debugging statement
            print(f"Logged-in user type: {request.user.user_type}")  # Debugging statement
            
            employee = form.save()
            print(f"Registered employee: {employee}")  # Debugging statement
            
            company = get_object_or_404(Company, user_id=request.user.pk)
            print(f"Associated company: {company}")  # Debugging statement
            
            employee.company = company
            employee.save()
            print(employee.company)
            messages.success(request, "Your employee was registered successfully!")
            print('to ekana')
            return redirect('list-employees')
        else:
            print('Form is invalid')
            print(form.errors)
    else:
        form = RegisterEmployeeForm()
    return render(request, 'vacayvue/register_employee.html', {'form': form})

def list_employees(request):
    company = get_object_or_404(Company, user_id=request.user.pk)
    print("Logged-in user:", request.user)  # Debugging statement
    print("Associated company:", company)  # Debugging statement
    
    employees = Employee.objects.filter(company=company)
    print("Employees:", employees)  # Debugging statement
    
    return render(request, 'vacayvue/list-employees.html', {'employees': employees})



def employee_home(request):
    employee = get_object_or_404(Employee, user_id=request.user.pk)

    return render(request, 'vacayvue/employee_home.html',{'employee': employee})


def company_home(request):
        company = get_object_or_404(Company, user_id=request.user.pk)
        return render(request, 'vacayvue/company_home.html',{'company': company})



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
            user = authenticate(request, email=email, password=password)
            print(f"Email received in login view: {email}")  # Debugging statement

            if user is not None:
                print(f'User authenticated: {user}')  # Debugging statement
                print(f'User type: {user.user_type}')  # Debugging statement

                login(request, user)
                if user.user_type == 'company':
                    return redirect('company_home')
                else:
                    return redirect('employee_home')  # Redirect employee to their home page
            else:
                messages.error(request, 'Invalid email, password')
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