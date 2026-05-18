from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "index.html")
def register_page(request):
    return render(request, "register.html")
def login_page(request):
    return render(request, "login.html")
def create_request_page(request):
    return render(request, "create-request.html")
def forget_password_page(request):
    return render(request, "forget-password.html")