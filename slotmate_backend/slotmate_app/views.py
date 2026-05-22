from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from .models import SlotRequest, StudentProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, "index.html" , {
        "user": request.user
    })

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        university = request.POST.get("university")
        department = request.POST.get("department")

        username = email.split('@')[0]
        
        if User.objects.filter(username=username).exists():
         return render(request, "register.html", {"error": "User already exists! Please use another email."} )
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        StudentProfile.objects.create(
            user=user,
            university=university,
            department=department
        )
        return redirect('/login/')
    
    return render(request, "register.html")

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email.split('@')[0], password=password)
       
        if user is not None:
            login(request, user)
            return redirect("/index/")
        else:
            return render(request, "login.html", {"error": "Invalid email or password."})

    return render(request, "login.html")

def create_request_page(request):
    if request.method == "POST":
        SlotRequest.objects.create(
            user=request.user,
            #Current slot
            current_course_code=request.POST.get("currentCourse"),
            current_section=request.POST.get("currentSection"),
            current_faculty=request.POST.get("currentFaculty"),
            current_time=request.POST.get("currentTime"),
            current_days=request.POST.get("currentDay"),

        #Preferred slot info
            preferred_course_code=request.POST.get("preferredCourse"),
            preferred_section=request.POST.get("preferredSection"),
            preferred_faculty=request.POST.get("preferredFaculty"),
            preferred_time=request.POST.get("preferredTime"),
            preferred_days=request.POST.get("preferredDay"),
        
        #Any Options
            any_day=bool(request.POST.get("any_day")),
            any_time=bool(request.POST.get("any_time")),
            any_section=bool(request.POST.get("any_section")),
            any_faculty=bool(request.POST.get("any_faculty"))
        )
        return redirect("/index/")
    return render(request, "create-request.html")

def forget_password_page(request):
    return render(request, "forget-password.html")
def my_requests_page(request):
    return render(request, "my-requests.html")
def matches_page(request):
    return render(request, "matches.html")
def notifications_page(request):
    return render(request, "notifications.html")
def profile_page(request):
    return render(request, "profile.html")
