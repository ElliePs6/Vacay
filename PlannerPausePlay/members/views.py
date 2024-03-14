from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
#from .forms import LoginForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)             
        if user is not None:
                #Redirect to a success page
                login(request, user)
                return redirect('home')
        else:
             #Return an 'invalid login' error message
             messages.success(request,('Υπήρχε κάποιο λάθος στη συνδεσή σας. Προσπαθηστε ξανα..'))
             return redirect ('login') 
            
    else:
         return render(request, 'authenticate/login.html', {})



