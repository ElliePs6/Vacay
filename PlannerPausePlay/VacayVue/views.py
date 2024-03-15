from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Requests,Employees,Events
from .forms import RequestForm
from django.http import JsonResponse
from django.utils import timezone 



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
 
def update_request(request, request_id):
    request = request.objects.get(pk=request_id)
    return render(request, 'vacayvue/update_request.html',{'request':request})


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




