from django.shortcuts import render, redirect
from .models import Requests,Employee,Events,CustomUser,Company
from .forms import RequestForm,LoginForm,RegisterEmployeeForm
from django.http import JsonResponse, Http404, HttpResponseServerError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize




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
    try:
        events = Events.objects.all()
        # Serialize event objects into JSON format
        event_data = serialize('json', events)
        # Return serialized data as JsonResponse
        return JsonResponse(event_data, safe=False)
    except Exception as e:
        # Log the error for debugging purposes
        print(f'An error occurred in all_events view: {str(e)}')
        # Return an appropriate HTTP response
        return HttpResponseServerError('An error occurred while processing the request')
    

def add_event(request):
    try:
        title = request.GET.get("title")
        start = request.GET.get("start")
        end = request.GET.get("end")
        
        event = Events.objects.create(name=title, start=start, end=end)
        return JsonResponse({'id': event.id})
    except Exception as e:
        print(f'An error occurred in add_event view: {str(e)}')
        return HttpResponseServerError('An error occurred while adding the event')

def update(request):
    try:
        id = request.GET.get("id")
        event = Events.objects.get(id=id)
        event.title = request.GET.get("title")
        event.start = request.GET.get("start")
        event.end = request.GET.get("end")
        event.save()
        return JsonResponse({})
    except Exception as e:
        print(f'An error occurred in update view: {str(e)}')
        return HttpResponseServerError('An error occurred while updating the event')

def remove(request):
    try:
        id = request.GET.get("id")
        Events.objects.filter(id=id).delete()
        return JsonResponse({})
    except Exception as e:
        print(f'An error occurred in remove view: {str(e)}')
        return HttpResponseServerError('An error occurred while removing the event')
 

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