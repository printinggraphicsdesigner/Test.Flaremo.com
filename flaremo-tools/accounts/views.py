from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from .models import EmailOTP
from .utils import generate_otp


# ================= LOGIN =================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_active:
                return render(request, 'accounts/login.html', {
                    'error': 'Account not verified. Please check your email.'
                })

            login(request, user)
            return redirect('/account/dashboard/')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


# ================= REGISTER =================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match
        if password != confirm_password:
            return render(request, 'accounts/register.html', {
                'error': 'Passwords do not match'
            })

        # Username check
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists'
            })

        # Email check
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Email already exists'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_active = False
        user.save()

        # Delete old OTP (important)
        EmailOTP.objects.filter(user=user).delete()

        # Generate OTP
        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)

        # Send Email
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect(f'/verify-otp/{user.id}/')

    return render(request, 'accounts/register.html')


# ================= VERIFY OTP =================
from django.utils import timezone
from datetime import timedelta

def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).last()

        if otp_obj:
            # Expire check (5 min)
            if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
                return render(request, 'accounts/verify_otp.html', {
                    'error': 'OTP expired',
                    'user_id': user.id
                })

            if otp_obj.otp == otp_input:
                user.is_active = True
                user.save()
                otp_obj.delete()

                login(request, user)  # auto login 🔥
                return redirect('/account/dashboard/')

        return render(request, 'accounts/verify_otp.html', {
            'error': 'Invalid OTP',
            'user_id': user.id
        })

    return render(request, 'accounts/verify_otp.html', {
        'user_id': user.id
    })


# ================= DASHBOARD =================
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'accounts/dashboard.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('/')