import pytz
from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomSignupForm, ProfileForm



class SignUp(SignupView):
    model = User
    form_class = CustomSignupForm
    success_url = reverse_lazy('account_login')
    template_name = 'registration/signup.html'


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    extra_context = {
        "timezones": pytz.common_timezones,
    }

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


def set_timezone(request):
    if request.method == "POST":
        request.session["django_timezone"] = request.POST["timezone"]
        return redirect("profile")
    else:
        return render(request, "accounts/set_timezone.html", {"timezones": pytz.common_timezones, })
