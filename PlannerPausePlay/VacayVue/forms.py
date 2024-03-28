from django import forms
from django.forms import ModelForm
from .models import Requests,Employee,CustomUser,Company
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)

class RegisterEmployeeForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Joining Date', 'id': 'date_joined'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'title': 'Your password must contain at least 8 characters and cannot be too similar to your other personal information.'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'title': 'Please enter the same password for verification.'})
    )
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'date_joined', 'password1', 'password2', 'first_name', 'last_name','company']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employee'

        if commit:
            user.save()
            Employee.objects.create(
                    user=user,
                    join_date=self.cleaned_data['date_joined'],
                    company = self.cleaned_data.get('company')
                )

        return user


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

