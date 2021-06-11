from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


gender_choices = (
    ('m', 'male'),
    ('fm', 'female'),
    ('o', 'other'),

)


class ExtendedUser(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'username_id'}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name',
        'id': 'username_id'}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name',
        'id': 'username_id'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={

        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'username_id'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={

        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'username_id'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={

        'class': 'form-control',
        'placeholder': ' Confirm Password',
        'id': 'username_id'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    # def save(self, commit=True):
    #     user=super().save(commit=False)

    #     if commit:
    #         user.save()
    #     return user


class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'date of birth',
            'id': 'username_id'}))
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'id': 'username_id'}))

    profile_pic=forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'dob', 'gender']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'username_id'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password_id',
        }
    ))
