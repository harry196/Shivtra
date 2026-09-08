import email

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TripBooking, Booking


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()

        # Dummy AI Logic
        if "jaipur" in user_message:
            bot_reply = "Jaipur is the Pink City of India. Famous for Hawa Mahal, Amber Fort, and royal palaces."
        
        elif "udaipur" in user_message:
            bot_reply = "Udaipur is known as the City of Lakes. Lake Pichola and City Palace are major attractions."
        
        elif "jaisalmer" in user_message:
            bot_reply = "Jaisalmer is the Golden City. You can enjoy desert safari and camel rides."
        
        elif "hello" in user_message or "hi" in user_message:
            bot_reply = "Hello! How can I help you with Rajasthan travel today?"
        
        else:
            bot_reply = "Sorry, I can help with Rajasthan destinations like Jaipur, Udaipur, and Jaisalmer."

        return JsonResponse({"response": bot_reply})


# ============================
# BASIC PAGES
# ============================

def home(request):
    if request.method == "POST":
        from_place = request.POST.get("from_place")
        to_place = request.POST.get("to_place")
        travel_date = request.POST.get("travel_date")
        transport_mode = request.POST.get("transport_mode")

        TripBooking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            from_place=from_place,
            to_place=to_place,
            travel_date=travel_date,
            transport_mode=transport_mode
        )

        messages.success(request, "Trip search submitted successfully")
        return redirect("home")

    return render(request, "home.html")


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')


# ============================
# AUTHENTICATION
# ============================

#def login_user(request):
    #if request.method == "POST":
        #username = request.POST.get("username")
        #password = request.POST.get("password")

        #user = authenticate(username=username, password=password)

        #if user:
            #login(request, user)
           # return redirect('home')

        #return render(request, 'login.html', {"error": "Invalid credentials"})

    #return render(request, 'login.html')


#def signup_user(request):
   # if request.method == "POST":
       # User.objects.create_user(
           # username=request.POST.get("username"),
           # password=request.POST.get("password")
       # )
        #return redirect('login')

   #return render(request, 'signup.html')

#def home_view(request):
   # show_welcome = request.session.pop('show_welcome', False)
   # welcome_type = request.session.pop('welcome_type', 'login')
    #return render(request, 'home.html', {
      #  'show_welcome': show_welcome,
       # 'welcome_type': welcome_type,
   # })


# ============================
# LOGOUT
# ============================

#def logout_user(request):
    #logout(request)
    #return redirect('home')

# ============================
# SEARCH
# ============================

def search_trips(request):
    if request.method != "POST":
        return redirect("home")

    from_place = request.POST.get("from_place")
    to_place = request.POST.get("to_place")
    travel_date = request.POST.get("travel_date")
    transport_mode = request.POST.get("transport_mode")

    trips = [
        {
            "from": from_place,
            "to": to_place,
            "date": travel_date,
            "mode": transport_mode,
            "price": 1200,
            "duration": "6h 30m"
        },
        {
            "from": from_place,
            "to": to_place,
            "date": travel_date,
            "mode": transport_mode,
            "price": 1600,
            "duration": "5h 45m"
        }
    ]

    return render(request, "search_results.html", {
        "trips": trips
    })



# ============================
# BOOKINGS
# ============================

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-booked_on")
    return render(request, "booking_history.html", {"bookings": bookings})


def state_detail(request, state_slug):
    states_data = {
        'uttar-pradesh': {
            'name': 'Uttar Pradesh',
            'tagline': 'Spiritual Escape',
            'places': [
                {'name': 'Kashi (Varanasi)', 'image': 'img/KASHI.jpg', 'class':'img-top img-fixed', 'info': 'The spiritual capital of India, famous for Ganga Aarti and ancient temples.', 'location': 'Varanasi, UP'},
                {'name': 'Ayodhya', 'image': 'img/ayodhya.jpeg', 'class':'img-top img-fixed', 'info': 'Birthplace of Lord Ram, home to the grand Ram Mandir.', 'location': 'Ayodhya, UP'},
                {'name': 'Prayagraj', 'image': 'img/prayagraj.jpeg', 'class':'img-top img-fixed', 'info': 'The holy Sangam city where three sacred rivers meet.', 'location': 'Prayagraj, UP'},
                {'name': 'Mathura-Vrindavan', 'image': 'img/mathura.jpeg', 'class':'img-top img-fixed', 'info': 'Land of Lord Krishna, filled with colorful temples and festivals.', 'location': 'Mathura, UP'},
                {'name': 'Lucknow', 'image': 'img/lucknow.jpeg', 'class':'img-top img-fixed', 'info': 'City of Nawabs — rich in culture, cuisine, and architecture.', 'location': 'Lucknow, UP'},
                {'name': 'Agra', 'image': 'img/agra.jpeg', 'info': 'Home of the iconic Taj Mahal, a wonder of the world.', 'location': 'Agra, UP'},
            ]
        },
        'rajasthan': {
            'name': 'Rajasthan',
            'tagline': 'Royal Heritage',
            'places': [
                {'name': 'Jaipur', 'image': 'img/jaipur.jpeg', 'info': 'The Pink City — palaces, forts, and vibrant bazaars.', 'location': 'Jaipur, Rajasthan'},
                {'name': 'Udaipur', 'image': 'img/udaipur.jpeg', 'info': 'City of Lakes — romance, royalty, and stunning views.', 'location': 'Udaipur, Rajasthan'},
                {'name': 'Jodhpur', 'image': 'img/jodhpur.jpeg', 'info': 'The Blue City — Mehrangarh Fort and desert charm.', 'location': 'Jodhpur, Rajasthan'},
                {'name': 'Jaisalmer', 'image': 'img/jaisalmer.jpeg', 'info': 'The Golden City — desert safaris and ancient havelis.', 'location': 'Jaisalmer, Rajasthan'},
            ]
        },
        'odisha': {
            'name': 'Odisha',
            'tagline': 'Divine Odisha',
            'places': [
                {'name': 'Puri', 'image': 'img/puri.jpeg', 'info': 'Home of Lord Jagannath Temple and beautiful beaches.', 'location': 'Puri, Odisha'},
                {'name': 'Konark', 'image': 'img/konark.jpeg', 'info': 'The Sun Temple — a UNESCO World Heritage masterpiece.', 'location': 'Konark, Odisha'},
                {'name': 'Bhubaneswar', 'image': 'img/bhubaneswar.jpeg', 'info': 'Temple City of India with hundreds of ancient shrines.', 'location': 'Bhubaneswar, Odisha'},
            ]
        },
        'jammu-kashmir': {
            'name': 'Jammu & Kashmir',
            'tagline': 'Nature Retreat',
            'places': [
                {'name': 'Srinagar', 'image': 'img/srinagar.jpeg', 'info': 'Dal Lake houseboats, Mughal gardens, and snow-capped peaks.', 'location': 'Srinagar, J&K'},
                {'name': 'Gulmarg', 'image': 'img/gulmarg.jpeg', 'info': 'Ski paradise and the world\'s highest golf course.', 'location': 'Gulmarg, J&K'},
                {'name': 'Pahalgam', 'image': 'img/pahalgam.jpeg', 'info': 'Valley of Shepherds — trekking, rivers, and serenity.', 'location': 'Pahalgam, J&K'},
                {'name': 'Vaishno Devi', 'image': 'img/vaishnodevi.jpeg', 'info': 'One of the holiest Hindu pilgrimage sites in the mountains.', 'location': 'Katra, J&K'},
            ]
        },
        'maharashtra': {
            'name': 'Maharashtra',
            'tagline': 'Heritage and Hills',
            'places': [
                {'name': 'Mumbai', 'image': 'img/mumbai.jpeg', 'info': 'City of Dreams — Gateway of India, Marine Drive, Bollywood.', 'location': 'Mumbai, Maharashtra'},
                {'name': 'Pune', 'image': 'img/pune.jpeg', 'info': 'Cultural capital with forts, food, and history.', 'location': 'Pune, Maharashtra'},
                {'name': 'Lonavala', 'image': 'img/lonavala.jpeg', 'info': 'Hill station with waterfalls, caves, and misty views.', 'location': 'Lonavala, Maharashtra'},
                {'name': 'Ajanta-Ellora', 'image': 'img/ajanta.jpeg', 'info': 'UNESCO caves with stunning ancient rock-cut art.', 'location': 'Aurangabad, Maharashtra'},
            ]
        },
        'uttarakhand': {
            'name': 'Uttarakhand',
            'tagline': 'Yoga & Peace',
            'places': [
                {'name': 'Rishikesh', 'image': 'img/rishi.jpg', 'info': 'Yoga capital of the world — adventure and spirituality.', 'location': 'Rishikesh, Uttarakhand'},
                {'name': 'Haridwar', 'image': 'img/haridwar.jpeg', 'info': 'Gateway to Gods — Ganga Aarti at Har Ki Pauri.', 'location': 'Haridwar, Uttarakhand'},
                {'name': 'Nainital', 'image': 'img/nainital.jpeg', 'info': 'Lake city surrounded by hills and colonial charm.', 'location': 'Nainital, Uttarakhand'},
                {'name': 'Mussoorie', 'image': 'img/mussoorie.jpeg', 'info': 'Queen of Hills — waterfalls, trails, and panoramic views.', 'location': 'Mussoorie, Uttarakhand'},
            ]
        },
    }

    state = states_data.get(state_slug)
    if not state:
        return render(request, '404.html', status=404)
    return render(request, 'state_detail.html', {'state': state})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')

    return redirect('home')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("home")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("home")

        # ✅ THIS LINE HASHES PASSWORD CORRECTLY
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()
        messages.success(request, "Account created successfully")
        return redirect("home")

    return redirect("home")

def home_view(request):
    show_welcome = request.session.pop('show_welcome', False)
    welcome_type = request.session.pop('welcome_type', 'login')
    return render(request, 'home.html', {
        'show_welcome': show_welcome,
        'welcome_type': welcome_type,
    })

def logout_view(request):
    logout(request)
    return redirect('home')