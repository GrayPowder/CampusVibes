from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django import forms
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings


def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def homepage(request):
    return render(request, 'homepage.html')


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            if request.FILES.get('avatar'):
                user.profile.avatar = request.FILES['avatar']
                user.profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

        if 'update_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('profile')

        if 'update_password' in request.POST:
            messages.error(request, 'Please fix the errors below.')
    else:
        profile_form = ProfileUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'user_avatar': user.profile.avatar.url if hasattr(user, 'profile') and user.profile.avatar else '/static/images/logo/user.png'
    })


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


def password_reset_onepage(request, uidb64=None, token=None):
    context = {}
    if uidb64 is None:
        form = PasswordResetForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            users = list(form.get_users(form.cleaned_data['email']))
            if users:
                user = users[0]
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(f"/forgot-password/{uid}/{token}/")
                send_mail(
                    subject="Password Reset Request",
                    message=f"Hi {user.username},\n\nUse the link below to reset your password:\n{reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                context['message'] = f"A password reset link has been sent to {user.email}!"
            else:
                context['error'] = "No account with that email."
        context['form'] = form
        context['step'] = 'email'
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        if user and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST or None)
            if request.method == 'POST' and form.is_valid():
                form.save()
                context['message'] = "Your password has been reset successfully!"
                return redirect('login')
            context['form'] = form
            context['step'] = 'reset'
        else:
            context['error'] = "Invalid or expired link."

    return render(request, 'forgot_password.html', context)