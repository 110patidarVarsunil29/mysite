from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import UserProfile


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user


# Sending mail


class ContactForm(forms.Form):
    full_name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows': 80, 'cols': 20}),
    )


# Managing files

class Profile_Form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'fname',
            'display_picture'
        ]
