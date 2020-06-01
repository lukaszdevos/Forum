from django.shortcuts import render,redirect,get_object_or_404
from django.http import request, HttpResponseRedirect,HttpRequest
from accounts.forms import SignUpForm, ProfileForm, UserUpdateForm
#login/logout
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
#profiledashboard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DetailView, View, FormView
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView,PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator

class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

# DASHBOARD

def profile_details_view(request,username):
    if request.user.is_anonymous:
        return redirect("accounts:login")

    elif request.user.username == username:
        user_name = User.objects.get(username=username)
        context = {'profile':user_name}
        return render(request, 'accounts/profile.html', context)

    return redirect('/profile/' + request.user.username)


def profile_edit_view(request):
    if request.user.is_anonymous:
        return redirect("accounts:login")

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        update_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and update_form.is_valid():
            if not request.user.profile.profile_img:
                request.user.profile.profile_img = 'default.jpg'

            profile_form.save()
            update_form.save()

            return redirect('/profile/' + request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        update_form = UserUpdateForm(instance=request.user)


    context = {'profile_form':profile_form,
               'update_form':update_form }

    return render(request, 'accounts/profile_edit.html', context)


def change_password(request):
    template_name = 'accounts/profile_change_password.html'

    if request.user.is_anonymous == True:
        return redirect("accounts:login")

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile/' + request.user.username)
    else:
        form = PasswordChangeForm(request.user)

    context = {'form':form}

    return render(request, template_name, context)


class PasswordReset(PasswordResetView):
    model = User
    template_name= "accounts/password_reset_form.html"
    form_class = PasswordResetForm
    email_template_name = "accounts/password_reset_email.html"
    token_generator = default_token_generator
    success_url = "/password_reset_done/" 


class PasswordResetDone(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    model = User
    form_class = SetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    token_generator = default_token_generator
    success_url = '/password_reset_complete/'
    from_email = ('Django web')
    title = ('Password reset   {{user.username}}')

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
