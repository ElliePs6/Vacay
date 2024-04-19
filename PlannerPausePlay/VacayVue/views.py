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




#-----------------Συναρτήσεις για το ημερολογιο----------------------------------------------------

def delete_request(request, request_id):
    event = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def update(request):
    if request.method == 'GET':
        start = request.GET.get("start")
        end = request.GET.get("end")
        request_type = request.GET.get("type")
        request_id = request.GET.get("id")
        # Check if all required data is present
        if start and end and request_type and request_id:
            try:
                request_obj = Request.objects.get(pk=request_id)
                # Update the request fields
                request_obj.start = start
                request_obj.end = end
                request_obj.type = request_type
                request_obj.save()
                return JsonResponse({'message': 'Request updated successfully'})
            except Request.DoesNotExist:
                return JsonResponse({'error': 'Request with id  does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'Missing required data'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    

def add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            print("Form is valid.")
            request_object = form.save(commit=False)
            request_object.user = request.user
            request_object.save()
            print("Request object saved successfully.")
            return JsonResponse({'success': True})
        else:
            print("Form validation failed. Errors:", form.errors)
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        print("Received non-POST request. Method:", request.method)
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@login_required
def all_requests(request):
    user = request.user
    user_requests = Request.objects.filter(user=user)  
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

    
def calendar(request):  
    form = RequestForm()  
    all_requests = Request.objects.all()
    context = {
        "form": form,  # Pass the form to the context
        "all_requests": all_requests,
    }
    return render(request, 'vacayvue/request_calendar.html', context)   


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
    form =EditEmployeeForm(request.POST or None, instance=employee)
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
    print("Logged-in user:", request.user)  # Debugging statement
    print("Associated company:", company)  # Debugging statement
    
    employees_list = Employee.objects.filter(company=company)
    print("Employees_list:", employees_list)  # Debugging statement
    
    return render(request, 'vacayvue/list-employees.html', {'employees_list': employees_list})

@login_required
def employee_home(request):
    employee = get_object_or_404(Employee, user_id=request.user.pk)

    return render(request, 'vacayvue/employee_home.html',{'employee': employee})

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


#---------------Συναρτήσεις για αιτήσεις----------------------------------------------
@login_required
def self_requests(request):
     employee = get_object_or_404(CustomUser, email=request.user.email)
     requests=Request.objects.filter(user_id=employee)
     return render(request, 'vacayvue/self-requests.html', { 'requests':requests} )

@login_required
def list_all_requests(request):
    company = get_object_or_404(Company, user=request.user)
    employees = Employee.objects.filter(company=company)
    user_ids = employees.values_list('user_id', flat=True)
    requests = Request.objects.filter(user_id__in=user_ids)
    return render(request, 'vacayvue/list-all-requests.html', {'requests': requests})

#-----------------HomePage Company-------------------------------------------------------

def approve_request(request):
    if request.method == 'POST' and request.is_ajax():
        request_id = request.POST.get('request_id')
        try:
            req = Request.objects.get(pk=request_id)
            req.is_approved = True
            req.is_pending = False
            req.save()
            messages.success(request, 'Request has been approved successfully.')
            return JsonResponse({'success': True})
        except Request.DoesNotExist:
            return JsonResponse({'success': False})

def reject_request(request):
    if request.method == 'POST' and request.is_ajax():
        request_id = request.POST.get('request_id')
        try:
            req = Request.objects.get(pk=request_id)
            req.is_rejected = True
            req.is_pending = False
            req.save()
            messages.warning(request, 'Request has been rejected.')
            return JsonResponse({'success': True})
        except Request.DoesNotExist:
            return JsonResponse({'success': False})


@login_required
def company_home(request):
        company = get_object_or_404(Company, user_id=request.user.pk)
        return render(request, 'vacayvue/company_home.html',{'company': company})

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