from django import forms
from django.forms import ModelForm
from .models import Requests

#Create a form
class RequestForm(ModelForm):
    class Meta:
        model= Requests
        #fields= "__all__"/Ta painei ola ta pedia apo to model
        fields=('StartDate','EndDate','Type','Comments')
        labels = { 
            'StartDate':"",
            'EndDate':"",
            'Type':"",
            'Comments':""
        }
        widgets = {
            'StartDate':forms.DateInput(attrs={'class':'form-control','placeholder':'Ημερομηνία Έναρξης'}),
            'EndDate':forms.DateInput(attrs={'class':'form-control','placeholder':'Ημερομηνία Λήξης'}),
            'Type':forms.TextInput(attrs={'class':'form-control','placeholder':'Τύπος Άδειας'}),
            'Comments':forms.TextInput(attrs={'class':'form-control','placeholder':'Σχόλια'})
        }
