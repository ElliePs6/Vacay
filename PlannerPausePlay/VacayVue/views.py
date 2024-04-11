from django.shortcuts import render, redirect
from .models import Request,Company,CustomUser,Employee
from .forms import RequestForm,LoginForm,RegisterEmployeeForm
from django.http import JsonResponse, Http404, HttpResponseServerError, HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.utils import timezone
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
        "all_requests": all_requests,
    }

    return render(request, 'vacayvue/request_calendar.html', context)


def all_requests(request):
    user = request.user
    user_requests = Request.objects.filter(user=user)  # Assuming there's a ForeignKey field named 'user' in your Request model
    out = []                                                                                                             
    for request_obj in user_requests:                                                                                             
        out.append({                                                                                                     
            'type': request_obj.type,                                                                                         
            'id': request_obj.id,                                                                                              
            'start': request_obj.start.strftime("%Y-%m-%d") if request_obj.start else None,
            'end': request_obj.end.strftime("%Y-%m-%d") if request_obj.end else None, 
            'description': request_obj.description,                                                 
        })
                                                                                                             
                                                                                                                      
    return JsonResponse(out, safe=False)

def add_request(request):
    # Create a form instance and populate it with data from the request (binding)
    form = RequestForm(request.POST)
    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        request_object = form.save(commit=False) 
        request_object.user = request.user  
        request_object.save() 
        return JsonResponse({'success': True})

    else:
        
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})



def delete_request(request, request_id):
    event = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)



    
def edit_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    if request.method == 'GET':
        context = {'form': RequestForm(instance=request_obj), 'request_id': request_id}
        return render(request,'vacayvue/edit_request.html',context)




def list_requests(request):
     company = get_object_or_404(Company, user_id=request.user.pk)
     all_requests=Request.objects.filter(company=company)
     return render(request, 'vacayvue/list-requests.html',
        { 'all_requests':all_requests})
'''
def list_requests(request):
     employee = get_object_or_404(Employee, user_id=request.user.pk)
     all_requests=Request.objects.filter(employee=employee)
     return render(request, 'vacayvue/list-requests.html',
        { 'all_requests':all_requests})
        '''



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