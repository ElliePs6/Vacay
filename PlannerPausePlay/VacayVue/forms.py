from django import forms
from django.forms import ModelForm
from .models import Requests

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