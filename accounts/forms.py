from django import forms
from django.contrib.auth import authenticate

class RecruiterLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
            if user.user_type !='recruiter' and not user.is_superuser:
                raise forms.ValidationError("You are not authorized to login as recruiter")
            cleaned_data['user'] = user
        return cleaned_data