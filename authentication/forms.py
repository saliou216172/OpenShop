
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "name", "email", "phone", "profile", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input-field',
                'placeholder': field.label
            })

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")

    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': "Non d'utilisateur "
            })
        self.fields['password'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': "Mot de passe "
        })