from django import forms
from django.forms import ModelForm
from .models import Request,CustomUser,Employee,LeaveType
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('employee', 'Employee'), ('company', 'Company')), required=True)


class RegisterEmployeeForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control','placeholder': 'Email'}))
    join_date = forms.DateField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Ημερομηνία Πρόσληψης', 'id': 'id_join_date'}),
    input_formats=['%d/%m/%Y']  # Adjusted format
)
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip', 'placeholder': 'Κωδικός','title': 'Your password must contain at least 8 characters and cannot be too similar to your other personal information.'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'tooltip','placeholder': 'Επιβεβαίωση Κωδικού','title': 'Please enter the same password for verification.'})
    )
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Όνομα'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Επίθετο'}))
    
    class Meta:
        model = CustomUser
        fields = ['email', 'join_date', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.user_type = 'employee'
        if commit:
            user.save()
            employee=Employee.objects.create(
            user=user,#1 user is employee user
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            join_date=self.cleaned_data['join_date'],
            )
        return employee

class EditEmployeeForm(forms.ModelForm):
    join_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Ημερομηνία Πρόσληψης', 'id': 'id_join_date'}),
        input_formats=['%Y-%m-%d']  # Format expected by Django
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'join_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }


#-------------------------------------------------------------------------------------------------------------------------------------------

CHOICES = (
        ('Κανονική Άδεια', 'Κανονική Άδεια'),
        ('Αδεια Εξετάσεων Εργαζόμενων Σπουδαστών', 'Αδεια Εξετάσεων Εργαζόμενων Σπουδαστών'),
        ('Αδεια Εξετάσεων Μεταπτυχιακών Φοιτητών', 'Αδεια Εξετάσεων Μεταπτυχιακών Φοιτητών'),
        ('Αιμοδοτική Άδεια', 'Αιμοδοτική Άδεια'),
        ('Άδεια Άνευ Αποδοχών', 'Άδεια Άνευ Αποδοχών'),
        ('Άδεια Μητρότητας', 'Άδεια Μητρότητας'),
        ('Άδεια Πατρότητας', 'Άδεια Πατρότητας'),
    )
MONTH_CHOICES = (
        (1, 'Ιανουάριος'),(2, 'Φεβρουάριος'),(3, 'Μάρτιος'),(4, 'Απρίλιος'),
        (5, 'Μάιος'),(6, 'Ιούνιος'),(7, 'Ιούλιος'),(8, 'Αύγουστος'),
        (9, 'Σεπτέμβριος'),(10, 'Οκτώβριος'),(11, 'Νοέμβριος'),(12, 'Δεκέμβριος'),
    )

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name', 'default_days', 'reset_month']
        widgets ={
            'default_days':forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d*','placeholder': 'xxxx'}),
             'name': forms.Select(choices=CHOICES),
             'reset_month': forms.Select(choices=MONTH_CHOICES)
             }
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        reset_month = cleaned_data.get('reset_month')
        user = self.instance.user if self.instance and hasattr(self.instance, 'user') else None
        if self.instance and self.instance.pk:  # If updating an existing LeaveType
            return cleaned_data  # Skip validation for updates
        if name and reset_month and user:
            if LeaveType.objects.filter(user=user, name=name).exists():
                raise forms.ValidationError("A LeaveType with this name already exists for this user.")
            existing_leave_types = LeaveType.objects.filter(user=user)
            if existing_leave_types.exists() and reset_month != existing_leave_types.first().reset_month:
                raise forms.ValidationError({'reset_month': 'The reset month must be consistent for leave types with the same user.'})
        return cleaned_data

class RequestForm(ModelForm):
    leave_type = forms.ModelChoiceField(queryset=LeaveType.objects.none())  # Empty initial queryset

    start =forms.DateField(
       widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Ημερομηνία Έναρξης', 'id': 'id_start'}),
       input_formats=['%d/%m/%Y']  # Adjusted format
    )

    end = forms.DateField(
       widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Ημερομηνία Λήξης', 'id': 'id_end'}),
       input_formats=['%d/%m/%Y']  # Adjusted format
    )


    class Meta:
        model = Request
        fields = ["leave_type", "start", "end", "description"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Περιγραφή Αιτήσεως",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leave_type'].queryset = LeaveType.objects.all()
        default_leave_type = LeaveType.objects.filter(name='Κανονική Άδεια').first()
        if default_leave_type:
            self.initial['leave_type'] = default_leave_type
#---------------------------------------------------------------------------------------#
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    