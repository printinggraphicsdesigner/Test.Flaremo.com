from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_otp_email(user, otp):
    subject = "Verify your account - Flaremo"

    text_content = f"Your OTP is: {otp}"

    html_content = f"""
    <div style="font-family: Arial; max-width:600px; margin:auto; padding:20px;">
        <h2 style="color:#ff6a00;">Flaremo Email Verification</h2>
        <p>Hello {user.username},</p>
        <p>Your OTP code is:</p>

        <h1 style="background:#f4f4f4; padding:15px; text-align:center; letter-spacing:5px;">
            {otp}
        </h1>

        <p>This OTP will expire in 5 minutes.</p>

        <p style="font-size:12px; color:#888;">
            If you did not request this, please ignore this email.
        </p>
    </div>
    """

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()