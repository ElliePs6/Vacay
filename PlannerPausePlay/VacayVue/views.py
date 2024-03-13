from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Requests,Employees,Events
from .forms import RequestForm
from django.http import JsonResponse 



def index(request):  
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'vacayvue/index.html',context)
 
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'event_id': event.event_id,                                                                                              
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
    event_id = request.GET.get("event_id", None)
    event = Events.objects.get(even_id=event_id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    event_id = request.GET.get("event_id", None)
    event = Events.objects.get(event_id=event_id)
    event.delete()
    data = {}
    return JsonResponse(data)
 

def list_employees(request):
    all_requests=Employees.objects.all()
    return render(request, 'vacayvue/list-employees.html',
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



def list_requests(request):
    all_requests=Requests.objects.all()
    return render(request, 'vacayvue/list-requests.html',
        { 'all_requests':all_requests})


def home(request):
     return render(request, 'vacayvue/home.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                # Set user as staff (not sure if this is intended)
                user.is_staff = True
                user.save()
                return redirect('login_user')
        else:
            messages.error(request, "Passwords don't match")
            return redirect('register')
    else:
        # Handle GET request or other methods if needed
        return render(request, 'vacayvue/register.html')

    

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f'Successfully authenticated user: {user.username}')
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid login credentials.')
    else:
        form = LoginForm()

    return render(request, 'vacayvue/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')


