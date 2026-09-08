from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
import random

# ✅ OTP generator
def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(request):
    print("VIEW HIT")

    if request.method == "POST":
        print("POST REQUEST RECEIVED")

        identifier = request.POST.get('identifier', '').strip()
        print("IDENTIFIER:", identifier)

        otp = generate_otp()
        print("OTP GENERATED:", otp)

        request.session['otp'] = otp
        request.session['identifier'] = identifier

        if "@" in identifier:
            print("EMAIL OTP PATH")
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is {otp}",
                from_email=None,
                recipient_list=[identifier],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email")
        else:
            print("MOBILE OTP PATH")
            messages.success(request, f"Dummy OTP sent: {otp}")

        return redirect('verify_otp')

    return render(request, 'otp/send_otp.html')


def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if user_otp == session_otp:
            request.session.flush()
            messages.success(request, "OTP verified successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'otp/verify_otp.html')
