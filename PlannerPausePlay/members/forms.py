from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    Firstname = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    Lastname = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model  = User
        fields = ('username', 'Firstname', 'Lastname', 'email','password1','password2')

    def __init__(self,*args, **kwargs):
        super(RegisterUserForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'