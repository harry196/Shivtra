
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
import random




# =====================================================
# NORMAL USER LOGIN (USERNAME + PASSWORD)
# =====================================================
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "home.html")

        if not user.is_active:
            messages.error(request, "Please verify your email before logging in.")
            return render(request, "home.html")

        login(request, user)

        request.session.set_expiry(1209600 if remember else 0)
        messages.success(request, f"Welcome back, {user.username}!")
        return render(request, "home.html")

    return render(request, "login.html")


# =====================================================
# USER SIGNUP (EMAIL VERIFICATION REQUIRED)
# =====================================================
def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "home.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "home.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "home.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )
        user.save()

        send_verification_email(request, user)
        messages.success(request, "Account created. Please verify your email.")
        return render(request, "home.html")

    return render(request, "signup.html")


# =====================================================
# EMAIL VERIFICATION
# =====================================================
def send_verification_email(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = f"http://{current_site.domain}/accounts/verify-email/{uid}/{token}/"

    send_mail(
        subject="Verify your email",
        message=f"Click to verify your account:\n{verify_url}",
        from_email=None,
        recipient_list=[user.email],
    )


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully.")
    else:
        messages.error(request, "Invalid or expired verification link.")

    return render(request, "home.html")


# =====================================================
# LOGOUT
# =====================================================
def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return render(request, "home.html")


# =====================================================
# DUMMY GOOGLE LOGIN (NO PASSWORD, AUTO VERIFIED)
# =====================================================
def dummy_google_login(request):
    """
    Simulates Google OAuth login (DEV ONLY)
    """

    google_email = "demo.google.user@gmail.com"
    full_name = "Google Demo User"

    user, created = User.objects.get_or_create(
        email=google_email,
        defaults={
            "username": google_email.split("@")[0],
            "first_name": "Google",
            "last_name": "User",
            "is_active": True,
        }
    )

    if created:
        user.set_unusable_password()
        user.save()

    login(request, user)
    messages.success(request, "Logged in with Google.")
    return render(request, "home.html")


# =====================================================
# EMAIL OTP LOGIN (GMAIL / EMAIL DUMMY)
# =====================================================
def send_email_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = str(random.randint(100000, 999999))

        OTP.objects.create(contact=email, otp=otp) # type: ignore
        request.session["email_otp"] = email

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is {otp}",
            from_email=None,
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email.")
        return redirect("verify_email_otp")

    return render(request, "send_email_otp.html")


def verify_email_otp(request):
    email = request.session.get("email_otp")

    if not email:
        messages.error(request, "Session expired.")
        return redirect("send_email_otp")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        try:
            otp_obj = OTP.objects.filter(contact=email).latest("id") # type: ignore
        except OTP.DoesNotExist: # type: ignore
            messages.error(request, "OTP not found.")
            return redirect("send_email_otp")

        if otp_obj.otp != entered_otp:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_email_otp")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "is_active": True,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        login(request, user)
        messages.success(request, "Logged in via Email OTP.")
        return redirect("home")

    return render(request, "verify_email_otp.html")


# =====================================================
# MOBILE OTP LOGIN
# =====================================================
def send_mobile_otp(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        otp = str(random.randint(100000, 999999))

        OTP.objects.create(contact=mobile, otp=otp) # type: ignore
        request.session["mobile_otp"] = mobile

        messages.success(request, f"OTP sent (DEV): {otp}")
        return redirect("verify_mobile_otp")

    return render(request, "send_mobile_otp.html")


def verify_mobile_otp(request):
    mobile = request.session.get("mobile_otp")

    if not mobile:
        messages.error(request, "Session expired.")
        return redirect("send_mobile_otp")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        try:
            otp_obj = OTP.objects.filter(contact=mobile).latest("id") # type: ignore
        except OTP.DoesNotExist: # type: ignore
            messages.error(request, "OTP not found.")
            return redirect("send_mobile_otp")

        if otp_obj.otp != entered_otp:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_mobile_otp")

        user, created = User.objects.get_or_create(
            username=f"user_{mobile}",
            defaults={
                "is_active": True,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        login(request, user)
        messages.success(request, "Logged in via Mobile OTP.")
        return render(request, "home.html")

    return render(request, "verify_mobile_otp.html")
