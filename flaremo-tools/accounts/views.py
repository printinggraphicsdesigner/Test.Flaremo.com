from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import EmailOTP
from .utils import generate_otp, send_otp_email


# ================= LOGIN (EMAIL BASED) =================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            if not user.is_active:
                return render(request, 'accounts/login.html', {
                    'error': 'Account not verified. Please verify OTP.'
                })

            login(request, user)
            # 👇 Remember me logic
            if not remember:
                request.session.set_expiry(0) 
            return redirect('/account/dashboard/')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid email or password'
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


        # Delete old OTP
        EmailOTP.objects.filter(user=user).delete()

        # Generate OTP
        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)

        try:
            send_otp_email(user, otp)
        except Exception as e:
            print(f"Email sending failed: {e}")
   

        # ✅ সুন্দর HTML email send
        send_otp_email(user, otp)

        return redirect(f'/account/verify-otp/{user.id}/')

    return render(request, 'accounts/register.html')


# ================= VERIFY OTP =================
def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).last()

        if otp_obj:
            # ⏱ Expire check (5 min)
            if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
                return render(request, 'accounts/verify_otp.html', {
                    'error': 'OTP expired',
                    'user_id': user.id
                })

            # ✅ Match OTP
            if otp_obj.otp == otp_input:
                user.is_active = True
                user.save()
                otp_obj.delete()

                login(request, user)  # auto login
                return redirect('/account/dashboard/')

        return render(request, 'accounts/verify_otp.html', {
            'error': 'Invalid OTP',
            'user_id': user.id
        })

    return render(request, 'accounts/verify_otp.html', {
        'user_id': user.id
    })


# ================= RESEND OTP =================
def resend_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    last_otp = EmailOTP.objects.filter(user=user).last()

    # ⛔ 30 sec limit
    if last_otp and timezone.now() - last_otp.created_at < timedelta(seconds=30):
        return render(request, 'accounts/verify_otp.html', {
            'error': 'Please wait 30 seconds before requesting new OTP',
            'user_id': user.id
        })

    # Delete old OTP
    EmailOTP.objects.filter(user=user).delete()

    # Generate new OTP
    otp = generate_otp()
    EmailOTP.objects.create(user=user, otp=otp)

    # Send email
    send_otp_email(user, otp)

    return render(request, 'accounts/verify_otp.html', {
        'success': 'New OTP sent to your email',
        'user_id': user.id
    })

 # ================= FORGOT PASSWORD =================
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'Email not found'
            })

        # Delete old OTP
        EmailOTP.objects.filter(user=user).delete()

        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)

        send_otp_email(user, otp)

        return redirect(f'/reset-password/{user.id}/')

    return render(request, 'accounts/forgot_password.html')



# ================= RESET PASSWORD =================
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')  # 👈 add this

        otp_obj = EmailOTP.objects.filter(user=user).last()

        # ✅ OTP check আগে
        if otp_obj and otp_obj.otp == otp_input:

            # ✅ 👇 password match check (এইখানে বসবে)
            if new_password != confirm_password:
                return render(request, 'accounts/reset_password.html', {
                    'error': 'Passwords do not match',
                    'user_id': user.id
                })

            # ✅ optional: length check
            if len(new_password) < 6:
                return render(request, 'accounts/reset_password.html', {
                    'error': 'Password must be at least 6 characters',
                    'user_id': user.id
                })

            # ✅ সব ঠিক হলে save
            user.set_password(new_password)
            user.save()

            otp_obj.delete()

            return redirect('/login/')

        else:
            return render(request, 'accounts/reset_password.html', {
                'error': 'Invalid OTP',
                'user_id': user.id
            })

    return render(request, 'accounts/reset_password.html', {
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
