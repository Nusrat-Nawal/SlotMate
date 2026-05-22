from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from .models import StudentProfile

# Create your views here.
def home(request):
    return render(request, "index.html")

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
    return render(request, "login.html")
def create_request_page(request):
    return render(request, "create-request.html")
def forget_password_page(request):
    return render(request, "forget-password.html")