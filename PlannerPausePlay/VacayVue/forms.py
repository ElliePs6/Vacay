from django import forms
from django.forms import ModelForm
from .models import Requests,Employees,CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm


class RequestForm(ModelForm):
    class Meta:
        model = Requests
        fields = ('Type', 'StartDate', 'EndDate', 'Comments')
        labels = { 
            'Type': "",
            'StartDate': "",
            'EndDate': "",            
            'Comments': ""
        }
        widgets = {
            'Type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Τύπος Άδειας'}),
            'StartDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Ημερομηνία Έναρξης', 'id': 'start-date'}),
            'EndDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Ημερομηνία Λήξης', 'id': 'end-date'}),
            'Comments': forms.TextInput(attrs={'class': 'form-control comments', 'placeholder': ''})
        }

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)

class RegisterEmployeeForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Joining Date', 'id': 'date_joined'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'title': 'Your password must contain at least 8 characters and cannot be too similar to your other personal information.'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'title': 'Please enter the same password for verification.'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'date_joined', 'password1', 'password2']
        labels = {'date_joined': "Joining Date"}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.user_type = 'employee'

        if commit:
            user.save()
            Employees.objects.create(
            user=user,
            join_date=self.cleaned_data['date_joined'],
            username=self.cleaned_data['username']
        )

        return user