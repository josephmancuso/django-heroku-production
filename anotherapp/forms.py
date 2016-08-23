from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length='32', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length='32', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class NewUserForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password:', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email:", max_length=120, widget=forms.EmailInput(attrs={'class': 'form-control'}))
