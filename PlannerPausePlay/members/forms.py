from django import forms
from django.contrib.auth.forms import UserCreationForm
from VacayVue.models import CustomUser, Company
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator




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
        user.user_type = 'διαχειριστής'
        if commit:
            user.save()
        return user

# Custom validator for AFM
validate_afm = RegexValidator(r'^\d{9}$', 'Το ΑΦΜ πρέπει να είναι 9 ψηφία.', 'invalid')

class RegisterCompanyForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
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
    afm = forms.CharField(label='ΑΦΜ',
                           validators=[validate_afm], max_length=9, 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d*'}),
                           error_messages={'required': 'Παρακαλώ συμπληρώστε το πεδίο ΑΦΜ.'}
                           )
    dou = forms.CharField(max_length=50, label='DOU', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'name', 'hr_name', 'afm', 'dou')

    def clean_afm(self):
        afm = self.cleaned_data.get('afm')
        if afm:
            try:
                Company.objects.get(afm=afm)
                raise forms.ValidationError('Το ΑΦΜ αυτό έχει ήδη χρησιμοποιηθεί.')
            except Company.DoesNotExist:
                pass
        return afm

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        hr_name = cleaned_data.get('hr_name')
        afm = cleaned_data.get('afm')
        dou = cleaned_data.get('dou')

        # Check if all required fields from the Company model are filled
        if not (name and hr_name and afm and dou):
            raise forms.ValidationError('Please fill out all required fields.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  
        user.user_type = 'εταιρία'

        if commit:
            user.save()
            Company.objects.create(
                user=user, 
                name=self.cleaned_data['name'],
                hr_name=self.cleaned_data['hr_name'],
                afm=self.cleaned_data['afm'],
                dou=self.cleaned_data['dou']
            )

        return user