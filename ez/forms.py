from django import forms

class PasswordForm(forms.Form):
    repository_password = forms.CharField(label='Password', max_length=100)
