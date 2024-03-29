from django import forms
from django.contrib.auth.forms import UserCreationForm
from VacayVue.models import CustomUser, Company
from django.contrib.auth.forms import UserCreationForm


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
        user.user_type = 'admin'
        if commit:
            user.save()
        return user

class RegisterCompanyForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True,'class': 'form-control'}))
    name = forms.CharField(max_length=255, label='Company Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    hr_name = forms.CharField(max_length=255, label='HR Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
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
        fields = ('email', 'password1', 'password2', 'name', 'hr_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set username as email
        user.user_type = 'company'

        if commit:
            user.save()
            # Create associated Companies instance
            Company.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                hr_name=self.cleaned_data['hr_name']
            )

        return user

