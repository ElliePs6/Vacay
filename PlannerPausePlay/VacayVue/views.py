from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import Request,Company,CustomUser,Employee, LeaveType,Balance
from .forms import RequestForm,LoginForm,RegisterEmployeeForm,EditEmployeeForm, LeaveTypeForm,ChangePasswordForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags





#from datetime import datetime
#from django.forms import modelformset_factory
#from django.db import IntegrityError
#from django.db.models import Sum
#from django.db.models import F, ExpressionWrapper, DurationField,FloatField
#from django.db.models import Count
#import json
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
        leave_type = request.leave_type.name.strip().lower()  # Convert to lowercase
        color = get_color_for_request(leave_type)
        print(f"Leave Type: {leave_type}, Color: {color}")  # Add this line for debugging
        event = {
            'title': f"{employee.user.get_full_name()} - {leave_type}",
            'start': request.start.strftime('%Y-%m-%d'),
            'end': request.end.strftime('%Y-%m-%d'),
            'color': color
        }
        events.append(event)

    return JsonResponse(events, safe=False)


def get_color_for_request(request_leave_type):
    color_map = {
        'κανονική άδεια':'#C40C0C',
        'αδεια εξετάσεων εργαζόμενων σπουδαστών':'#FF6500',
        'αδεια εξετάσεων μεταπτυχιακών φοιτητών':'#FF8A08', 
        'αιμοδοτική άδεια': '#FFC100',
        'άδεια άνευ αποδοχών':'#C08B5C',
        'άδεια μητρότητας':'#795458', 
        'άδεια πατρότητας':'#453F78',
    }
    return color_map.get(request_leave_type, '#7777')  

@login_required
def calendar(request):  
    all_requests = Request.objects.all()
    context = {
        "all_requests": all_requests,
    }
    return render(request, 'vacayvue/company_home.html', context)

#------------------------------------------Συναρτήσεις για αιτήσεις----------------------------------------------------

@login_required
def add_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user            
            # Check if the requested number of days exceeds the default days
            leave_type = form.cleaned_data['leave_type']
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
            requested_days = (end_date - start_date).days + 1
            if leave_type.default_days < requested_days:
                raise ValidationError("Η διάρκεια της άδειας υπερβαίνει τις προεπιλεγμένες μέρες.")            
            # Check remaining days for the user and leave type
            if Request.objects.filter(user=request.user, leave_type=leave_type, is_approved=True).exists():
                remaining_days = Balance.objects.filter(user=request.user, leave_type=leave_type).values_list('remaining_days', flat=True).first()
                print("Remaining days:", remaining_days)
                if remaining_days is not None and remaining_days < requested_days:
                    raise ValidationError("Οι υπόλοιπες ημέρες δεν επαρκούν για το αίτημα άδειας.")            
            request_instance.save()
            return redirect('my_requests')
    else:
        form = RequestForm()
    return render(request, 'vacayvue/add_request.html', {'form': form})

@login_required
def leave_request_success(request):
    return render(request, 'leave_request_success.html')

@login_required
def leave_request_rejected(request):
    return render(request, 'leave_request_rejected.html')

@login_required
def approve_leave_request(request, request_id):  
        leave_request = Request.objects.get(id=request_id)
        leave_request.is_approved = True
        leave_request.is_rejected = False
        leave_request.is_pending = False
        leave_request.save()
        update_balance_on_approval(leave_request)
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
     return render(request, 'vacayvue/my_requests.html', context)


@login_required
def request_details(request, request_id):
     request_obj = get_object_or_404(Request, pk=request_id)
     return render(request, 'vacayvue/request_details.html', {'request': request_obj})

@login_required
def list_all_requests(request):
    company = get_object_or_404(Company, user=request.user)
    employees = Employee.objects.filter(company=company)
    user_ids = employees.values_list('user_id', flat=True)
    requests = Request.objects.filter(user_id__in=user_ids,is_approved=True )
    context={
        'requests': requests,
 }
    return render(request, 'vacayvue/list_requests.html',context )

#----------------------------------------Settings/Balance-------------------------------------------------------------------

@login_required
def manage_leave_type(request):
    if request.method == "POST":
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            leave_type_instance = form.save(commit=False)
            leave_type_instance.user = request.user
            leave_type_instance.save()
            # Set default days and update balance
            set_default_days(leave_type_instance, request.user, leave_type_instance.default_days)
            return redirect('manage_leave_type')
    else:
        form = LeaveTypeForm()

    leave_types = LeaveType.objects.filter(user=request.user)
    
    # Ensure balances are created for each leave type
    for leave_type in leave_types:
        balance, created = Balance.objects.get_or_create(user=request.user, leave_type=leave_type)
        if created:
            balance.default_days = leave_type.default_days
            balance.save()

    return render(request, 'vacayvue/manage_leave_type.html', {'form': form, 'leave_types': leave_types})



from django.db.models import Sum

@require_GET
def balance_data(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Get all leave types
        leave_types = LeaveType.objects.all()
        balance_data = []

        for leave_type in leave_types:
            try:
                
                leave_type = request.leave_type.name.strip().lower()
                balance = Balance.objects.filter(user=request.user, leave_type=leave_type).aggregate(
                    usedDays=Sum('used_days'), totalDays=Sum('default_days'))
                balance_data.append({
                    'leave_type': leave_type.name,
                    'usedDays': balance['usedDays'] if balance['usedDays'] is not None else 0,
                    'totalDays': balance['totalDays'] if balance['totalDays'] is not None else leave_type.default_days
                })
            except Balance.DoesNotExist:
                # If balance data doesn't exist, add default values
                balance_data.append({
                    'leave_type': leave_type.name,
                    'usedDays': 0,
                    'totalDays': leave_type.default_days
                })

        # Return the constructed JSON response outside the loop
        return JsonResponse({'balance_data': balance_data})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


# Function to set default days for a leave type and update balance
def set_default_days(leave_type, user, default_days):
    leave_type.default_days = default_days
    leave_type.save()
    balance, created = Balance.objects.get_or_create(user=user, leave_type=leave_type)
    balance.default_days = default_days
    balance.save()

def update_balance_on_approval(request_instance):
    # Check if a Balance instance with the same leave_type already exists for the user
    existing_balance = Balance.objects.filter(user=request_instance.user, leave_type=request_instance.leave_type).first()
    if existing_balance:
        # If an existing instance is found, use its default_days
        default_days = existing_balance.default_days
    else:
        # If not, use the default_days from the leave_type associated with the request_instance
        default_days = request_instance.leave_type.default_days
    # Get or create the balance for the user and leave type
    balance, created = Balance.objects.get_or_create(user=request_instance.user, leave_type=request_instance.leave_type)
    # Calculate the approved days
    approved_days = (request_instance.end - request_instance.start).days + 1
    # Update the used_days field in the balance
    balance.used_days += approved_days
    # Calculate remaining days
    balance.remaining_days = default_days - balance.used_days
    balance.save()

@login_required
def update_default_days(request, leave_type_id):
    leave_type = LeaveType.objects.get(id=leave_type_id)
    if request.method == "POST":
        form = LeaveTypeForm(request.POST, instance=leave_type)
        if form.is_valid():
            # Save the form for the current leave type
            form.save()
            
            # Update the reset_month field for all leave types
            reset_month = form.cleaned_data['reset_month']
            LeaveType.objects.exclude(id=leave_type_id).update(reset_month=reset_month)
            
            return redirect('manage_leave_type')
    else:
        form = LeaveTypeForm(instance=leave_type)
    return render(request, 'vacayvue/update_default_days.html', {'form': form, 'leave_type': leave_type})



'''
def reset_leave_balances():
    current_month = timezone.now().month
    leave_types = LeaveType.objects.all()

    for leave_type in leave_types:
        if leave_type.reset_month == current_month:
            leave_balances = LeaveBalance.objects.filter(leave_type=leave_type)
            for balance in leave_balances:
                balance.balance = leave_type.default_days
                balance.save()
'''





#--------------------------------Συναρτήσεις για υπαλλήλους----------------------------------------------------------

@login_required
def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    custom_user = employee.user
    employee.delete()
    custom_user.delete()
    return redirect('list_employees')


@login_required
def update_employee(request, employee_id):
    # Retrieve the Employee instance
    employee = Employee.objects.get(pk=employee_id)
    custom_user = employee.user
    # Initialize the form with the Employee instance
    form = EditEmployeeForm(request.POST or None, instance=custom_user )
    if form.is_valid():
        # Save the form data to the Employee instance
        custom_user  = form.save()
        return redirect('list_employees')    
    return render(request, 'vacayvue/update_employee.html', {'employee': employee, 'form': form})

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
    return render(request, 'vacayvue/list_employees.html', {'employees_list': employees_list})

from django.contrib.auth import get_user_model


@login_required
def add_employee(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            company = get_object_or_404(Company, user_id=request.user.pk)
            employee.company = company
            employee.save()
            messages.success(request, "Your employee was registered successfully!")
            return redirect('list_employees')
        else:
            print("Form errors:", form.errors)
            print("Data received in POST:", request.POST)
            print("Invalid form data:", form.cleaned_data)
    else:
        form = RegisterEmployeeForm()
    return render(request, 'vacayvue/add_employee.html', {'form': form})



def send_temporary_password_email(from_email, to_email, temporary_password):
    subject = 'Προσωρινός Κωδικός'
    html_message = render_to_string('email_templates/temporary_pass_email.html', {'password': temporary_password})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


@login_required
def employee_home(request):
    employee = get_object_or_404(Employee, user_id=request.user.pk)
    balances = Balance.objects.filter(user=request.user)
    leave_types = LeaveType.objects.all()
    color_map = {}
    for leave_type in leave_types:
        leave_type_name = leave_type.name.strip().lower()  # Convert to lowercase
        color_map[leave_type_name] = get_color_for_request(leave_type_name)
    context ={
        'employee': employee,
        'balances': balances,
        'leave_types': leave_types,
        'color_map': color_map
    }
    return render(request, 'vacayvue/employee_home.html', context)

#----------------------------------Password-------------------------------------------#
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if request.user.check_password(current_password):
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # Update session with new password
                    messages.success(request, 'Your password was successfully updated!')
                    return redirect('employee_home')  # Redirect to user profile page
                else:
                    messages.error(request, 'New passwords do not match!')
            else:
                messages.error(request, 'Incorrect current password!')
    else:
        form = ChangePasswordForm()
    return render(request, 'vacayvue/change_password.html', {'form': form})

#-----------------------HomePage Company συναρτήσεις-------------------------------------------------------

@login_required
def company_home(request):
    company = get_object_or_404(Company, user_id=request.user.pk)
    employee_count = Employee.objects.filter(company=company).count()
    # Fetch all pending requests
    pending_requests = Request.objects.filter(is_pending=True)
    leave_types = LeaveType.objects.all()
    # Populate the color map for leave types
    color_map = {}
    for leave_type in leave_types:
        leave_type_name = leave_type.name.strip().lower()  # Convert to lowercase
        color_map[leave_type_name] = get_color_for_request(leave_type_name)
    context = {
        'employee_count': employee_count,
        'pending_requests': pending_requests,
        'company': company,
        'color_map': color_map
    }
    return render(request, 'vacayvue/company_home.html', context)




#-------------------------Συναρτήσεις για users----------------------------------------------------
@login_required
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
                if user.has_usable_password():  # Check if user has a permanent password
                    login(request, user)
                    if user.user_type == 'company':
                        return redirect('company_home')
                    else:
                        return redirect('employee_home')
                else:
                    messages.warning(request, 'Πρέπει να αλλάξετε τον προσωρινό κωδικό πρόσβασής σας.')
                    # Redirect to the change password page
                    return redirect('change_password')
            else:
                messages.error(request, 'Λάθος email ή κωδικός', )
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'vacayvue/login.html', {'form': form})

def main_home(request):
    #Get current year   
   
    return render(request, 'vacayvue/main_home.html')


#-----------------------------------------------------------------------------------
