from allauth.account.forms import SignupForm, PasswordField, LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control my-2 text-bg-dark',
            "placeholder": _("Username"),
            "autocomplete": "username"
        })
        self.fields['email'].widget = forms.TextInput(attrs={
            "class": 'form-control my-2 text-bg-dark',
            "type": "email",
            "placeholder": _("Email address"),
            "autocomplete": "email",
        })
        self.fields['email'].label = _('Email')
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control my-2 text-bg-dark',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control my-2 text-bg-dark',
            'placeholder': _('Repeat password')
        })

    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name='authors')
        user.groups.add(authors)

        subject = 'Добро пожаловать в наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=None,
            to=[user.email],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'class': 'form-control my-2 text-bg-dark',
            'placeholder': _('Username or email'),
            "autocomplete": "email"
        })
        self.fields['login'].label = _('Login')
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control my-2 text-bg-dark',
            'placeholder': _('Password')
        })
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input align-self-center'})


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label=_('Username'),
                               widget=forms.TextInput(attrs={'class': 'form-control my-2 text-bg-dark'}))
    email = forms.CharField(disabled=True, label='Email',
                            widget=forms.TextInput(attrs={'class': 'form-control my-2 text-bg-dark'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-2 mt-2 text-bg-dark'})
        }
