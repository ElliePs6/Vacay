from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .models import Request,Company,CustomUser,Employee
from .forms import RequestForm,LoginForm,RegisterEmployeeForm,EditEmployeeForm
from django.http import JsonResponse, Http404, HttpResponseServerError, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


#from django.core.serializers import serialize
#from django.utils import timezone
#from django.urls import reverse
#from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)


#-----------------Συναρτήσεις για το ημερολογιο---------------------------------------------------- 
@login_required
def all_requests(request):
    
    approved_requests = Request.objects.filter(is_approved=True)
    events = []
    for request in approved_requests:
        employee = Employee.objects.get(user=request.user) 
        event = {
            'title': f"{employee.user.get_full_name()} - {request.type}",  # Display the type of request as the event title
            'start': request.start.strftime('%Y-%m-%d'),  
            'end': request.end.strftime('%Y-%m-%d'),      
            'color': get_color_for_request(request.type)  
        }
        events.append(event)

    return JsonResponse(events, safe=False)

def get_color_for_request(request_type):
    color_map = {
        'κανονική άδεια': '#7d0a0a', 
        'άδεια εξετάσεων εργαζόμενων σπουδαστών': '#00ff00',  
        'άδεια εξετάσεων μεταπτυχιακών φοιτητών': '#0000ff', 
        'αιμοδοτική άδεια': '#ffff00',  
        'άδεια άνευ αποδοχών': '#ff00ff', 
        'άδεια μητρλοτητας': '#00ffff',  
        'άδεια πατρότητας': '#ff9900'   
    }
    return color_map.get(request_type, '#000000')  


def calendar(request):  
    all_requests = Request.objects.all()
    context = {
        "all_requests": all_requests,
    }
    return render(request, 'vacayvue/company_home.html', context)

#---------------Συναρτήσεις για αιτήσεις----------------------------------------------

@login_required
def add_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            start_date_str = form.cleaned_data['start']
            end_date_str = form.cleaned_data['end']
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # Associate the parsed dates with the form fields
            form.instance.start = start_date
            form.instance.end = end_date
            form.instance.user = request.user
            
            # Save the form data to the database
            form.save()
            
            # Redirect to a success page or URL
            return redirect('employee_home')  # Replace 'employee_home' with the actual URL name
    else:
        form = RequestForm()
    return render(request, 'vacayvue/add_request.html', {'form': form})


def leave_request_success(request):
    return render(request, 'leave_request_success.html')

def leave_request_rejected(request):
    return render(request, 'leave_request_rejected.html')

@login_required
def approve_leave_request(request, request_id):  
        leave_request = Request.objects.get(id=request_id)
        leave_request.is_approved = True
        leave_request.is_rejected = False
        leave_request.is_pending = False
        leave_request.save()
        return redirect('list_all_requests') 
    
@login_required
def reject_leave_request(request, request_id):
        leave_request = Request.objects.get(id=request_id)
        leave_request.is_approved = False
        leave_request.is_rejected = True
        leave_request.is_pending = False
        leave_request.save()
        return redirect('list_all_requests')

@login_required
def list_all_requests(request):
    company = get_object_or_404(Company, user=request.user)
    employees = Employee.objects.filter(company=company)
    user_ids = employees.values_list('user_id', flat=True)
    requests = Request.objects.filter(user_id__in=user_ids)
    return render(request, 'vacayvue/list-all-requests.html', {'requests': requests})



@login_required
def self_requests(request):
     employee = get_object_or_404(CustomUser, email=request.user.email)
     
     pending_requests = Request.objects.filter(user_id=employee,is_pending=True)
     rejected_requests = Request.objects.filter(user_id=employee,is_rejected=True)
     approved_requests = Request.objects.filter(user_id=employee,is_approved=True)

     context = {
        'approved_requests':approved_requests,
        'rejected_requests':rejected_requests,
        'pending_requests': pending_requests,
        'employee': employee,
        
     }

     return render(request, 'vacayvue/self-requests.html', context)


@login_required
def request_details(request, request_id):
     request_obj = get_object_or_404(Request, pk=request_id)
     return render(request, 'vacayvue/request_details.html', {'request': request_obj})



#-------------Συναρτήσεις για υπαλλήλους----------------------------------------------------------

@login_required
def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    custom_user = employee.user
    employee.delete()
    custom_user.delete()
    return redirect('list-employees')  # Redirect to the employee list page after successful deletion


@login_required
def edit_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    form =RegisterEmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
            form.save()
            return redirect('list-employees')    
    return render(request, 'vacayvue/edit_employee.html', {'employee':employee,'form': form})

@login_required
def employee_details(request, employee_id):
    employee_id = request.GET.get('employee_id')
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'vacayvue/employee_details.html',{'employee':employee} )

@login_required
def list_employees(request):
    company = get_object_or_404(Company, user_id=request.user.pk)    
    employees_list = Employee.objects.filter(company=company)
    print("Employees_list:", employees_list)  # Debugging statement
    return render(request, 'vacayvue/list-employees.html', {'employees_list': employees_list})

@login_required
def register_employee(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():        
            employee = form.save()
            company = get_object_or_404(Company, user_id=request.user.pk)
            employee.company = company
            employee.save()
            messages.success(request, "Your employee was registered successfully!")
            return redirect('list-employees')
        else:
            print(form.errors)
    else:
        form = RegisterEmployeeForm()
    return render(request, 'vacayvue/register_employee.html', {'form': form})

@login_required
def employee_home(request):
    employee = get_object_or_404(Employee, user_id=request.user.pk)
    return render(request, 'vacayvue/employee_home.html',{'employee':employee})



#-----------------HomePage Company συναρτήσεις-------------------------------------------------------
def company_home(request):
    company = get_object_or_404(Company, user_id=request.user.pk)
    
    employee_count =Employee.objects.filter(company=company).count()

    # Fetch all pending requests
    pending_requests = Request.objects.filter(is_pending=True)

    context = {
        'employee_count': employee_count,
        'pending_requests': pending_requests,
        'company': company
    }

    return render(request, 'vacayvue/company_home.html', context)



#-----------------Συναρτήσεις για users----------------------------------------------------

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

            if not CustomUser.objects.filter(email=email, user_type=user_type).exists():
                messages.error(request, f'Το email δεν ανήκει σε κανέναν λογιαριασμό {user_type} ')
                return redirect('login')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'company':
                    return redirect('company_home')
                else:
                    return redirect('employee_home')
            else:
                messages.error(request, 'Λάθος email ή κωδικός', )
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

