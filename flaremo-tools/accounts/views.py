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
            ser_obj = User.objects.filter(email=email).first()
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

        # ✅ old OTP delete
        EmailOTP.objects.filter(user=user).delete()

        # ✅ OTP generate FIRST
        otp = generate_otp()

        # ✅ save OTP
        EmailOTP.objects.create(user=user, otp=otp)

        # ✅ send email (safe way)
        try:
            send_otp_email(user, otp)
        except Exception as e:
            return render(request, 'accounts/register.html', {
                'error': f'Email failed: {str(e)}'
            })

        # after user create

        request.session['verify_user_id'] = user.id

        return redirect('/account/verify-otp/')

    return render(request, 'accounts/register.html')


# ================= VERIFY OTP =================
def verify_otp(request):
    user_id = request.session.get('verify_user_id')

    if not user_id:
        return redirect('/register/')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).last()

        if otp_obj and otp_obj.otp == otp_input:
            user.is_active = True
            user.save()
            otp_obj.delete()

            login(request, user)

            # session clear
            del request.session['verify_user_id']

            return redirect('/account/dashboard/')

        return render(request, 'accounts/verify_otp.html', {
            'error': 'Invalid OTP'
        })

    return render(request, 'accounts/verify_otp.html')


# ================= RESEND OTP =================
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404

def resend_otp(request):
    user_id = request.session.get('verify_user_id')

    # ❌ যদি session না থাকে
    if not user_id:
        return redirect('/register/')

    user = get_object_or_404(User, id=user_id)

    last_otp = EmailOTP.objects.filter(user=user).last()

    # ⛔ 30 sec limit (same as your old logic)
    if last_otp and timezone.now() - last_otp.created_at < timedelta(seconds=30):
        return render(request, 'accounts/verify_otp.html', {
            'error': 'Please wait 30 seconds before requesting new OTP'
        })

    # 🧹 old OTP delete
    EmailOTP.objects.filter(user=user).delete()

    # 🔢 new OTP
    otp = generate_otp()
    EmailOTP.objects.create(user=user, otp=otp)

    # 📧 send email
    try:
        send_otp_email(user, otp)
    except Exception as e:
        return render(request, 'accounts/verify_otp.html', {
            'error': f'Email failed: {str(e)}'
        })

    return render(request, 'accounts/verify_otp.html', {
        'success': 'New OTP sent to your email'
    })



# ================= FORGOT PASSWORD =================
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'Email not found'
            })

        # 🧹 Delete old OTP
        EmailOTP.objects.filter(user=user).delete()

        # 🔢 Generate OTP
        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)

        # 📧 Send email
        try:
            send_otp_email(user, otp)
        except Exception as e:
            return render(request, 'accounts/forgot_password.html', {
                'error': f'Email failed: {str(e)}'
            })

        # ✅ IMPORTANT: session এ user store
        request.session['reset_user_id'] = user.id

        # ✅ clean URL (no user_id)
        return redirect('/account/reset-password/')

    return render(request, 'accounts/forgot_password.html')



# ================= RESET PASSWORD =================
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta

def reset_password(request):
    # ✅ session থেকে user
    user_id = request.session.get('reset_user_id')

    if not user_id:
        return redirect('/account/forgot-password/')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        otp_obj = EmailOTP.objects.filter(user=user).last()

        if otp_obj:
            # ⏱️ OTP expire (5 min)
            if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
                return render(request, 'accounts/reset_password.html', {
                    'error': 'OTP expired'
                })

            # ✅ OTP match
            if otp_obj.otp == otp_input:

                # 🔐 password match
                if new_password != confirm_password:
                    return render(request, 'accounts/reset_password.html', {
                        'error': 'Passwords do not match'
                    })

                # 🔐 length check
                if len(new_password) < 6:
                    return render(request, 'accounts/reset_password.html', {
                        'error': 'Password must be at least 6 characters'
                    })

                # 💾 save password
                user.set_password(new_password)
                user.save()

                otp_obj.delete()

                # 🧹 session clear
                del request.session['reset_user_id']

                return redirect('/login/')

        # ❌ fallback
        return render(request, 'accounts/reset_password.html', {
            'error': 'Invalid OTP'
        })

    return render(request, 'accounts/reset_password.html')






# ================= DASHBOARD =================
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'accounts/dashboard.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('/')
