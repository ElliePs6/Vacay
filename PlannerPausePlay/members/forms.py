from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from VacayVue.models import CustomUser,Employees,Companies
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)


class RegisterCompanyForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Your password must contain at least 8 characters and cannot be too similar to your other personal information.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Please enter the same password for verification.'
    )
    companyname = forms.CharField(max_length=255, label='Company Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    hrname = forms.CharField(max_length=255, label='HR Name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'companyname', 'hrname')
        
    def __init__(self, *args, **kwargs):
        super(RegisterCompanyForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Company Email'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.user_type = 'company'
        if commit:
            user.set_password(password)  # Hash the password
            user.save()
            companyname = self.cleaned_data['companyname']
            hrname = self.cleaned_data['hrname']
        # Create a new company instance and save it
        company = Companies.objects.create(Email=user.email, Companyname=companyname, HRname=hrname)
        return user



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

