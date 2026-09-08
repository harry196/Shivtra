from django.urls import include, path
from Home import views
from .views import chatbot

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

   
    path('search/', views.search_trips, name='search_trips'),
    path('my-bookings/', views.booking_history, name='booking_history'),

    path('auth_modal_login/', views.login_view, name='auth_modal_login'),
    path('auth_modal_signup/', views.signup_view, name='auth_modal_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('state/<slug:state_slug>/', views.state_detail, name='state_detail'),
    path("chatbot/", chatbot, name="chatbot"),
]






