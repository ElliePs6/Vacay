from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from VacayVue.models import CustomUser,Employees

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)


class RegisterCompanyForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
        
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
        fields = ('username','email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterCompanyForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'


class RegisterEmployeeForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
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
        labels = {
            'date_joined': "Joining Date",
        }

