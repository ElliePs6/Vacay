from django import forms
from django.contrib.auth.forms import UserCreationForm
from VacayVue.models import CustomUser, Companies
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)


class RegisterCompanyForm(UserCreationForm):
    companyname = forms.CharField(max_length=255, label='Company Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    hrname = forms.CharField(max_length=255, label='HR Name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ( 'companyname', 'hrname')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set username as email
        user.user_type = 'company'
        if commit:
            user.save()
            # Create a corresponding Companies instance
            Companies.objects.create(user=user, companyname=self.cleaned_data['companyname'], hrname=self.cleaned_data['hrname'])
        return user


class RegisterEmployeeForm(UserCreationForm):
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Joining Date', 'id': 'date_joined'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        model = CustomUser
        fields = [ 'username', 'date_joined', 'password1', 'password2']
        labels = {
            'date_joined': "Joining Date",
        }
