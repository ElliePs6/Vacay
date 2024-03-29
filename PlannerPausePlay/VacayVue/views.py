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


def list_employees(request):
    employees = Employee.objects.filter(company=request.user.company) 
    return render(request, 'vacayvue/list_employees.html', {'employees': employees})




def register_employee(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST, request=request)
        if form.is_valid():
            company_id = request.GET.get('company_id')  # Assuming company ID passed in URL parameter
            employee = form.save(commit=False)  # Don't commit yet
            employee.user_type = 'employee'  # Set user type explicitly (optional)

            if company_id:
                try:
                    company = Company.objects.get(pk=company_id)
                    employee.company = company
                    employee.save()
                    messages.success(request, 'Registration successful!')
                    return redirect('list-employees')
                except Company.DoesNotExist:
                    messages.error(request, 'Invalid company provided!')
                    # Re-render form with error message
                    return render(request, 'vacayvue/register_employee.html', {'form': form})
            else:
                messages.error(request, 'Missing company information!')
                # Re-render form with error message
                return render(request, 'vacayvue/register_employee.html', {'form': form})

    else:
        form = RegisterEmployeeForm(request=request)
    return render(request, 'vacayvue/register_employee.html', {'form': form})



@login_required
def employee_home(request):
    employee = request.user.employee  # Directly access employee object
    company = employee.company  # Retrieve associated company
    return render(request, 'vacayvue/employee_home.html', {'employee': employee, 'company': company})


@login_required
def company_home(request, company_id):
  if company_id:  # Check if company_id is provided
    company = get_object_or_404(Company, pk=company_id)  # Fetch company if available
    employees = Employee.objects.filter(company=company)  # Filter employees
  else:
    # Handle case where company_id is not provided (optional)
    messages.info(request, 'Company information not available.')
    return redirect('login')  # Or some other action
  return render(request, 'vacayvue/company_home.html', {'employees': employees})





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

      # Authenticate the user based on user_type
      user = authenticate(request, email=email, password=password, user_type=user_type)

      # Check if authentication is successful
      if user is not None:
        login(request, user)
        # Redirect user based on user_type with company ID if applicable
        if user.user_type == 'company':
           company_id = user.company.id if user.company else None
           return redirect('company_home', company_id=company_id)
        else:
          return redirect('employee_home')  # Redirect employee to their home page
      else:
        # Invalid email, password, or user_type
        messages.error(request, 'Invalid email, password, or user type.')
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








