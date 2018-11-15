from django import forms

class PasswordForm(forms.Form):
    repository_password = forms.CharField(label='Password', max_length=100)

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class RepoForm(forms.Form):
    repository_name = forms.CharField(label='Repository Name', max_length=100)
