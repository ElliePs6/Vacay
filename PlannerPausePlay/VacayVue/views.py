from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import Request,Company,CustomUser,Employee, LeaveType,Balance,CustomHolidays
from .forms import RequestForm,LoginForm,RegisterEmployeeForm,EditEmployeeForm, LeaveTypeForm,ChangePasswordForm,CustomHolidayForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages

from datetime import datetime,date
from django.db.utils import IntegrityError

import json




#-----------------Συναρτήσεις για το ημερολογιο----------------------------------------------------
def all_requests(request):
    approved_requests = Request.objects.filter(is_approved=True)
    custom_holidays = CustomHolidays.objects.all()
    events = []

    for request in approved_requests:
        employee = Employee.objects.get(user=request.user)
        leave_type = request.leave_type.name.strip().lower()
        color = get_color_for_request(leave_type)
        event = {
            'title': f"{employee.user.get_full_name()} - {leave_type}",
            'start': request.start.strftime('%Y-%m-%d'),
            'end': request.end.strftime('%Y-%m-%d'),
            'color': color
        }
        events.append(event)

    for holiday in custom_holidays:
        event = {
            'title': holiday.name,
            'start': holiday.date.strftime('%Y-%m-%d'),
            'color': '#f1f1f1'  # Set a color for custom holidays
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


def add_custom_holiday(request):
    if request.method == 'POST':
        # Load JSON data from request body
        data = json.loads(request.body)
        form = CustomHolidayForm(data)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            
            # Get the current user
            user = request.user
            
            # Create CustomHolidays object with user information
            CustomHolidays.objects.create(user=user, name=name, date=date)
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Handle GET request if needed
        return JsonResponse({'success': False, 'message': 'Method not allowed'})
#------------------------------------------Συναρτήσεις για αιτήσεις----------------------------------------------------


@login_required
def add_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user            
            leave_type = form.cleaned_data['leave_type']
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
            requested_days = (end_date - start_date).days + 1
            if leave_type.default_days < requested_days:
                form.add_error('leave_type', "Η διάρκεια της άδειας υπερβαίνει τις προεπιλεγμένες μέρες.")
            elif Request.objects.filter(user=request.user, leave_type=leave_type, is_approved=True).exists():
                remaining_days = Balance.objects.filter(user=request.user, leave_type=leave_type).values_list('remaining_days', flat=True).first()
                if remaining_days is not None and remaining_days < requested_days:
                    form.add_error('leave_type', "Οι υπόλοιπες ημέρες δεν επαρκούν για το αίτημα άδειας.")
            else:
                request_instance.save()
                messages.success(request, 'Το αίτημά σας καταχωρήθηκε με επιτυχία.')
                return redirect('my_requests')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
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
def handle_leave_request(request, request_id, action):
    # Check if the request ID exists
    leave_request = get_object_or_404(Request, id=request_id)
    
    # Handle the approval action
    if action == 'approve':
        # Check if the leave request has a corresponding balance
        try:
            balance = Balance.objects.get(user=leave_request.user, leave_type=leave_request.leave_type)
        except Balance.DoesNotExist:
            return JsonResponse({'success': False, 'message': "Ο εργαζόμενος δεν έχει αρκετές ημέρες για αυτόν τον τύπο άδειας."})

        # Proceed with additional checks
        requested_days = (leave_request.end - leave_request.start).days + 1
        if requested_days <= balance.remaining_days:
            # Approve the leave request
            leave_request.is_approved = True
            leave_request.is_rejected = False
            leave_request.is_pending = False
            leave_request.save()
            update_balance_on_approval(leave_request)
            return JsonResponse({'success': True, 'message': 'Εγκρίθηκε το αίτημα με επιτυχία.'})
        else:
            return JsonResponse({'success': False, 'message': "Ο εργαζόμενος δεν έχει αρκετές ημέρες για αυτόν τον τύπο άδειας."})
    else:
        return JsonResponse({'success': False, 'message': 'Μη έγκυρη ενέργεια.'})



@login_required
def my_requests(request):
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
def delete_pending_request(request, request_id):
    request_obj = get_object_or_404(Request, pk=request_id, is_pending=True)
    request_obj.delete()
    messages.success(request, 'Το αίτημα διαγράφηκε με επιτυχία.')
    return redirect('my_requests')



@login_required
def request_details(request, request_id):
     request_obj = get_object_or_404(Request, pk=request_id)
     return render(request, 'vacayvue/request_details.html', {'request': request_obj})

@login_required
def list_all_requests(request):
    company = get_object_or_404(Company, user=request.user)
    employees = Employee.objects.filter(company=company)
    user_ids = employees.values_list('user_id', flat=True)
    approved_requests = Request.objects.filter(user_id__in=user_ids, is_approved=True)
    context = {
        'approved_requests': approved_requests,
    }
    return render(request, 'vacayvue/list_requests.html',context )

@login_required
def delete_request(request, request_id):
    request_instance = get_object_or_404(Request, pk=request_id)
    update_balance_on_deletion(request_instance)
    request_instance.delete()
    messages.success(request, 'Το αίτημα διαγράφηκε με επιτυχία.')
    return redirect('company_home')


def update_balance_on_deletion(request_instance):
    # Check if a Balance instance with the same leave_type already exists for the user
    existing_balance = Balance.objects.filter(user=request_instance.user, leave_type=request_instance.leave_type).first()
    
    if existing_balance:
        # Calculate the approved days
        approved_days = (request_instance.end - request_instance.start).days + 1

        # Update the used_days field in the balance
        existing_balance.used_days -= approved_days

        # Recalculate remaining days
        existing_balance.remaining_days = existing_balance.default_days - existing_balance.used_days

        # Save the balance
        existing_balance.save()


#----------------------------------------Settings/Balance-------------------------------------------------------------------

@login_required
def manage_leave_type(request):
    user = request.user
    reset_month = None
    leave_types = LeaveType.objects.filter(user=user)
    
    # Set update_mode based on whether leave types exist for the user
    update_mode = not leave_types.exists()

    if leave_types.exists():
        reset_month = leave_types.first().reset_month

    if request.method == "POST":
        form = LeaveTypeForm(request.POST, initial={'reset_month': reset_month, 'update_mode': update_mode})
        if form.is_valid():
            try:
                leave_type_instance = form.save(commit=False)
                leave_type_instance.user = user
                if not reset_month:
                    reset_month = form.cleaned_data['reset_month']
                leave_type_instance.reset_month = reset_month
                leave_type_instance.save()

                # Call set_default_days to ensure Balance is updated
                set_default_days(leave_type_instance, user, leave_type_instance.default_days)

                messages.success(request, 'Ο τύπος άδειας προστέθηκε με επιτυχία.')
                return redirect('manage_leave_type')
            except IntegrityError:
                messages.error(request, 'Ένας τύπος άδειας με αυτό το όνομα υπάρχει ήδη.')
        else:
            messages.error(request, 'Παρουσιάστηκε σφάλμα κατά την προσθήκη του τύπου άδειας.')
    else:
        form = LeaveTypeForm(initial={'reset_month': reset_month, 'update_mode': update_mode})

    return render(request, 'vacayvue/manage_leave_type.html', {'form': form, 'leave_types': leave_types})


# Function to set default days for a leave type and update balance
def set_default_days(leave_type, user, default_days):
    leave_type.default_days = default_days
    leave_type.save()
    balance, created = Balance.objects.get_or_create(user=user, leave_type=leave_type)
    balance.default_days = default_days
    balance.save()

@login_required
def update_default_days(request, leave_type_id):
    # Get the leave type associated with the current user
    leave_type = LeaveType.objects.filter(id=leave_type_id, user=request.user).first()
    if not leave_type:
        # Handle the case where the leave type does not exist for the current user
        messages.error(request, 'Ο τύπος άδειας δεν βρέθηκε ή ανήκει σε διαφορετικό χρήστη.')
        return redirect('manage_leave_type')

    # Set update_mode to True
    update_mode = True
    
    if request.method == "POST":
        form = LeaveTypeForm(request.POST, instance=leave_type, initial={'update_mode': update_mode})
        if form.is_valid():
            # Save the form for the current leave type
            leave_type_instance = form.save()

            # Update the reset_month field for all leave types
            if 'reset_month' in form.changed_data:
                reset_month = form.cleaned_data['reset_month']
                LeaveType.objects.filter(user=request.user).exclude(id=leave_type_id).update(reset_month=reset_month)

            messages.success(request, 'Οι προεπιλεγμένες ημέρες και μήνας επαναφοράς ενημερώθηκαν με επιτυχία.')
            return redirect('manage_leave_type')
        else:
            messages.error(request, 'Παρουσιάστηκε σφάλμα κατά την ενημέρωση των προεπιλεγμένων ημερών.')
    else:
        form = LeaveTypeForm(instance=leave_type, initial={'update_mode': update_mode})
    
    return render(request, 'vacayvue/update_default_days.html', {'form': form, 'leave_type': leave_type})




@require_GET
def balance_data(request):
    if request.GET.get('ajax') == 'true':
        # This is an AJAX request
        # Your existing logic for processing AJAX requests
        leave_types = LeaveType.objects.all()
        balance_data = []

        for leave_type in leave_types:
            balance = Balance.objects.filter(user=request.user, leave_type=leave_type).first()  # Fetch a single Balance object
            if balance:
                balance_data.append({
                    'leave_type': leave_type.name,
                    'usedDays': balance.used_days,
                    'totalDays': balance.default_days  # Use default_days instead of total_days
                })
            else:
                balance_data.append({
                    'leave_type': leave_type.name,
                    'usedDays': 0,
                    'totalDays': leave_type.default_days
                })
        return JsonResponse({'balance_data': balance_data})
    else:        
        # logic for handling regular page requests
        return JsonResponse({'error': 'Invalid request.'}, status=400)
    





def update_balance_on_approval(request_instance):
    # Check if a Balance instance with the same leave_type already exists for the user
    existing_balance = Balance.objects.filter(user=request_instance.user, leave_type=request_instance.leave_type).first()
    if existing_balance:
        # If an existing instance is found, use its default_days
        default_days = existing_balance.leave_type.default_days
    else:
        # If not, use the default_days from the leave_type associated with the request_instance
        default_days = request_instance.leave_type.default_days
    
    # Get or create the balance for the user and leave type
    balance, created = Balance.objects.get_or_create(user=request_instance.user, leave_type=request_instance.leave_type)
    
    # Calculate the approved days
    approved_days = (request_instance.end - request_instance.start).days + 1
    
    # Update the used_days field in the balance
    balance.used_days += approved_days
    
    # Update the default_days field in the balance to match the corresponding LeaveType
    balance.default_days = default_days
    
    # Calculate remaining days
    balance.remaining_days = default_days - balance.used_days
    
    balance.save()





def get_target_month(request):
    # Retrieve the user's leave type with the reset_month field
    leave_type = LeaveType.objects.filter(user=request.user).first()
    if leave_type:
        # Use the reset_month field to determine the target month
        target_month = date(date.today().year, leave_type.reset_month, 1)
        print("Target month before adjustment:", target_month)  # Print statement
        # If the target month has passed this year, set it for the next year
        if target_month < date.today():
            target_month = date(date.today().year + 1, leave_type.reset_month, 1)
            print("Target month adjusted for next year:", target_month)  # Print statement
    else:
        # If no leave type with reset_month is found, set a default target month
        target_month = date(date.today().year + 1, 1, 1)  # January 1st of next year as a default
        print("No leave type found. Default target month set for next year:", target_month)  # Print statement
        
    return JsonResponse({'target_month': target_month})


#--------------------------------Συναρτήσεις για υπαλλήλους----------------------------------------------------------

@login_required
def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    custom_user = employee.user
    employee.delete()
    custom_user.delete()
    messages.success(request, 'Ο υπάλληλος διαγράφηκε με επιτυχία.')
    return redirect('list_employees')


@login_required
def update_employee(request, employee_id):
    # Retrieve the Employee instance
    employee = Employee.objects.get(pk=employee_id)
    custom_user = employee.user
    # Initialize the form with the Employee instance
    form = EditEmployeeForm(request.POST or None, instance=custom_user)
    if form.is_valid():
        # Save the form data to the Employee instance
        custom_user = form.save()
        messages.success(request, 'Ο υπάλληλος ενημερώθηκε με επιτυχία.')
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


@login_required
def add_employee(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            company = get_object_or_404(Company, user_id=request.user.pk)
            employee.company = company
            employee.save()
            messages.success(request, 'Η εγγραφή υπαλλήλου ήταν επιτυχής.')
            return redirect('list_employees')
        else:
            messages.error(request, 'Παρουσιάστηκε σφάλμα κατά την εγγραφή του υπαλλήλου.')
    else:
        form = RegisterEmployeeForm()
    return render(request, 'vacayvue/add_employee.html', {'form': form})





@login_required
def employee_home(request):
    month_mapping = {
    'January': 'Ιανουάριος',
    'February': 'Φεβρουάριος',
    'March': 'Μάρτιος',
    'April': 'Απρίλιος',
    'May': 'Μάιος',
    'June': 'Ιούνιος',
    'July': 'Ιούλιος',
    'August': 'Αύγουστος',
    'September': 'Σεπτέμβριος',
    'October': 'Οκτώβριος',
    'November': 'Νοέμβριος',
    'December': 'Δεκέμβριος',
}
    employee = get_object_or_404(Employee, user_id=request.user.pk)
    balances = Balance.objects.filter(user=request.user)
    leave_types = LeaveType.objects.all()
    color_map = {}
    for leave_type in leave_types:
        leave_type_name = leave_type.name.strip().lower()  # Convert to lowercase
        color_map[leave_type_name] = get_color_for_request(leave_type_name)
    
    # Get the current month
    current_month = month_mapping[datetime.now().strftime('%B')] + ' ' + str(datetime.now().year)
    print("Current Month:", current_month)  # Added print statement
    
    reset_month_str = "Not set"
    if leave_type and leave_type.reset_month:
        reset_month_year = datetime.now().year+1   # Calculate the year for the reset month
        reset_month = leave_type.reset_month
        
        reset_month_str = f"{leave_type.get_reset_month_display()} {reset_month_year}"
        print("Reset Month:", reset_month_str)  # Added print statement


        
    # Check if the current month and year match the reset month and year
    
    if current_month == reset_month_str and datetime.now().year == reset_month_year:
        print("Reset Month and Year Match!")  # Added print statement
        Balance.objects.filter(user=request.user, used_days__gt=0).delete()
    else:
        print("Reset Month and Year Don't Match!") 

    context ={
        'employee': employee,
        'balances': balances,
        'leave_types': leave_types,
        'color_map': color_map,
        'current_month': current_month,
        'reset_month': reset_month_str,
    }
    return render(request, 'vacayvue/employee_home.html', context)


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
                messages.error(request, f'Το email δεν ανήκει σε κανέναν {user_type}.')
                return redirect('login')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.has_usable_password():  # Check if user has a permanent password
                    login(request, user)
                    messages.success(request, 'Επιτυχής σύνδεση.')
                    if user.user_type == 'εταιρία':
                        return redirect('company_home')
                    else:
                        return redirect('employee_home')
                else:
                    messages.warning(request, 'Πρέπει να αλλάξετε τον προσωρινό κωδικό πρόσβασής σας.')
                    # Redirect to the change password page
                    return redirect('change_password')
            else:
                messages.error(request, 'Λάθος email ή κωδικός.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'vacayvue/login.html', {'form': form})

def main_home(request):  
    return render(request, 'vacayvue/main_home.html')


#-----------------------------------------------------------------------------------
