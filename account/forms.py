from django import forms
from django.contrib.auth.models import User

from .models import Profile


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

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exist():
            raise forms.ValidationError('Email already used')

        return data

    class Meta:
        model = User
        fields = ["username", "first_name", 'email']


    # Метод для сравнения 2ух паролей
    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd["password2"]:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


# для корректировки имени и мэила
class UserEditForm(forms.ModelForm):

    def clean_email(self):

        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)

        if qs.exists():
            raise forms.ValidationError('Email already used')

        return data


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birds', 'photo']
