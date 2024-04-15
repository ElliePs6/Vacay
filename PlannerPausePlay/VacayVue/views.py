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
    if request.method == 'POST':
        print("Received POST request for adding a request.")
        # Create a form instance and populate it with data from the request (binding)
        form = RequestForm(request.POST)
        print("Form data received:", request.POST)  # Print the received form data
        # Check if the form is valid
        if form.is_valid():
            print("Form is valid.")
            # Save the form data to the database
            request_object = form.save(commit=False)
            request_object.user = request.user
            request_object.save()
            print("Request object saved successfully.")
            return JsonResponse({'success': True})
        else:
            print("Form validation failed. Errors:", form.errors)
            # Check the format of errors returned
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        print("Received non-POST request. Method:", request.method)
        # Handle non-POST requests appropriately
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)




def delete_request(request, request_id):
    event = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def update(request):
    print("Request method:", request.method)  # Debugging: Print request method
    
    if request.method == 'GET':
        # Extract data from the GET request
        start = request.GET.get("start")
        end = request.GET.get("end")
        request_type = request.GET.get("type")
        request_id = request.GET.get("id")
        
        print("Received data:")
        print("Start:", start)  # Debugging: Print start
        print("End:", end)  # Debugging: Print end
        print("Type:", request_type)  # Debugging: Print type
        print("ID:", request_id)  # Debugging: Print ID
        
        # Check if all required data is present
        if start and end and request_type and request_id:
            try:
                # Get the request object from the database
                request_obj = Request.objects.get(pk=request_id)
                
                # Update the request fields
                request_obj.start = start
                request_obj.end = end
                request_obj.type = request_type
                
                # Save the updated request
                request_obj.save()
                
                # Respond with a success message
                return JsonResponse({'message': 'Request updated successfully'})
            except Request.DoesNotExist:
                # Handle the case where the request with the provided ID does not exist
                return JsonResponse({'error': 'Request does not exist'}, status=404)
        else:
            # Handle the case where some data is missing in the request
            return JsonResponse({'error': 'Missing required data'}, status=400)
    else:
        # Handle the case where the request method is not GET
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


def list_requests(request):
     employee = get_object_or_404(CustomUser, email=request.user.email)
     requests=Request.objects.filter(user_id=employee)
     return render(request, 'vacayvue/list-requests.html', { 'requests':requests} )



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
                messages.error(request, 'Λάθος email ή κωδικός')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'vacayvue/login.html', {'form': form, 'messages': messages.get_messages(request)})


def main_home(request):
    #Get current year   
    current_year=datetime.now().year
    return render(request, 'vacayvue/main_home.html',{       
        'current_year':current_year,
        
    })