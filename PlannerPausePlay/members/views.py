from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


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

def logout_user(request):
    logout(request)
    messages.success(request,('Είσαι Αποσυνδεμένος'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()  #  form save method invocation
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # If authentication is successful, log the user in
                login(request, user)
                messages.success(request, "Η εγγραφή ήταν επιτυχής!!!")
                return redirect('home')
            else:
                # Authentication failed, handle accordingly
                messages.error(request, "Σφάλμα στην είσοδο.")
        else:
            # Form is not valid, handle accordingly
            messages.error(request, "Η φόρμα περιέχει λανθασμένα δεδομένα.")
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {'form': form})

