from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput
    )


    class Meta:
        model = User
        firlds = ["username", "first_name", 'emaill']


    # Метод для сравнения 2ух паролей
    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd["password2"]:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']

