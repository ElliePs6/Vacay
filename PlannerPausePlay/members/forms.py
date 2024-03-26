from django import forms
from django.contrib.auth.forms import UserCreationForm
from VacayVue.models import CustomUser, Companies,Employees
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)

class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True,'class': 'form-control'}))

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
        fields = ['email','password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set username as email
        user.is_admin = True  # Set is_admin flag to True
        if commit:
            user.save()
        return user

class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'is_admin', 'user_type', 'company')

class AdminUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'is_admin', 'user_type', 'company')

class RegisterCompanyForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True,'class': 'form-control'}))
    companyname = forms.CharField(max_length=255, label='Company Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    hrname = forms.CharField(max_length=255, label='HR Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'title': 'Your password must contain at least 8 characters and cannot be too similar to your other personal information.'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'title': 'Please enter the same password for verification.'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'companyname', 'hrname')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set username as email
        user.user_type = 'company'

        if commit:
            user.save()
            # Create associated Companies instance
            Companies.objects.create(
                user=user,
                companyname=self.cleaned_data['companyname'],
                hrname=self.cleaned_data['hrname']
            )

        return user

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