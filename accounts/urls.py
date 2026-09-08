from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),

    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),

    # OTP
    path('email-otp/', views.send_email_otp, name='send_email_otp'),
    path('verify-email-otp/', views.verify_email_otp, name='verify_email_otp'),

    path('mobile-otp/', views.send_mobile_otp, name='send_mobile_otp'),
    path('verify-mobile-otp/', views.verify_mobile_otp, name='verify_mobile_otp'),

    # Dummy Google
    path('google-login/', views.dummy_google_login, name='google_login'),
]

