from django.shortcuts import render, redirect
from .models import Request,Employee,CustomUser,Company
from .forms import RequestForm,LoginForm,RegisterEmployeeForm
from django.http import JsonResponse, Http404, HttpResponseServerError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.utils.timezone import is_aware
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist




def employee_navbar(request):
    return render(request, 'vacayvue/employee_navbar.html')

def company_navbar(request):
    return render(request, 'vacayvue/company_navbar.html')


def calendar(request):  
    form = RequestForm()  # Create an instance of the form
    all_requests = Request.objects.all()
    context = {
        "form": form,  # Pass the form to the context
        "requests": all_requests,
    }
    return render(request, 'vacayvue/request_calendar.html', context)

 
def all_requests(request):
    all_requests = Request.objects.all()
    out = []                                                                                                             
    for request in all_requests:                                                                                             
        out.append({                                                                                                     
            'type': request.type,                                                                                         
            'id': request.id,                                                                                              
            'start': request.start.strftime("%Y-%m-%d %H:%M:%S"),                                                         
            'end': request.end.strftime("%Y-%m-%d %H:%M:%S"),                                                            
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 


def add_request(request):
    # Create a form instance and populate it with data from the request (binding)
    form = RequestForm(request.POST)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        request_object = form.save(commit=False)  # Get the unsaved object
        request_object.user = request.user  # Assuming you have a ForeignKey to User
        request_object.save()  # Save the object

        # Return success response
        return JsonResponse({'success': True})

    else:
        # Return error response with form errors
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})


def remove(request):
    id = request.POST.get("id", None)
    try:
        request = Request.objects.get(id=id)
        request.delete()
        data = {'success': True}
    except ObjectDoesNotExist:
        data = {'success': False, 'error': 'Request does not exist'}
    return JsonResponse(data)


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


    



 

def list_requests(request):
    all_requests=Request.objects.all()
    return render(request, 'vacayvue/list-requests.html',
        { 'all_requests':all_requests})

def request_calendar(request):
   if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data["type"]
            description = form.cleaned_data["description"]
            start = form.cleaned_data["start"]
            end = form.cleaned_data["end"]
            comments = form.cleaned_data["comments"]  
            Request.objects.create(
                user=request.user,
                type=type,
                description=description,
                start=start,
                end=end,
                comments=comments,  
            )
            return HttpResponseRedirect(reverse("calendar"))
        else:
            form = RequestForm()
        return render(request, "request_calendar.html", {"form": form})



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