import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def generate_otp():
    """৬ ডিজিটের ওটিপি জেনারেট করে"""
    return str(random.randint(100000, 999999))

def send_otp_email(user_email, otp, username="User"):
    """ইউজারকে ইমেইল পাঠায়"""
    subject = "Verify your account - Flaremo"
    text_content = f"Your OTP is: {otp}"

    # HTML ডিজাইন আপনারটাই থাকছে
    html_content = f"""
    <div style="font-family: Arial; max-width:600px; margin:auto; padding:20px; border: 1px solid #eee; border-radius: 10px;">
        <h2 style="color:#6366f1;">Flaremo Email Verification</h2>
        <p>Hello {username},</p>
        <p>Your OTP code is:</p>
        <h1 style="background:#f4f4f4; padding:15px; text-align:center; letter-spacing:5px; border-radius: 5px;">
            {otp}
        </h1>
        <p>This OTP will expire in 5 minutes.</p>
        <p style="font-size:12px; color:#888;">
            If you did not request this, please ignore this email.
        </p>
    </div>
    """

    try:
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
