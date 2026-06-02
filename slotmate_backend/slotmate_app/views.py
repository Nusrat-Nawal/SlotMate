from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from .models import SlotRequest, StudentProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import SlotRequest, Match
from .matching import calculate_mutual_score
from django.db.models import Q
# Create your views here.

@login_required
def index(request):
    matches = Match.objects.filter(
        Q(user_a=request.user) | Q(user_b=request.user)
    ).order_by("-mutual_score")[:4]

    return render(request, "index.html" , {
        "user": request.user,
        "matches" : matches
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

    any_day = False
    any_time = False
    any_section = False
    any_faculty = False

    if request.method == "POST":

        if not request.POST.get("currentCourse") or not request.POST.get("currentSection"):
            return render(request, "create-request.html", {
                "error": "Current Course and Section are required!"
            })
        if not request.POST.get("preferredCourse"):
            return render(request, "create-request.html", {
                "error": "Preferred Course is required!"
            })       
        #To check duplicates
        exists = SlotRequest.objects.filter(
        user=request.user,
        current_course_code=request.POST.get("currentCourse"),
        current_section=request.POST.get("currentSection")
        ).exists()
        if exists:
         return render(request, "create-request.html", {
        "error": "You already have a request for this current course + section. Delete old one first."
         })
        
        any_day = request.POST.get("any_day") == "on"
        any_time = request.POST.get("any_time") == "on"
        any_section = request.POST.get("any_section") == "on"
        any_faculty = request.POST.get("any_faculty") == "on"

        preferred_faculty = request.POST.get("preferredFaculty") or None
        preferred_section = request.POST.get("preferredSection") or None
        preferred_time = request.POST.get("preferredTime") or None
        preferred_days = request.POST.get("preferredDay") or None

        new_request =SlotRequest.objects.create(
            user=request.user,
            # Current slot
            current_course_code=request.POST.get("currentCourse"),
            current_section=request.POST.get("currentSection"),
            current_faculty=request.POST.get("currentFaculty"),
            current_time=request.POST.get("currentTime"),
            current_days=request.POST.get("currentDay"),

            # Preferred slot info
            preferred_course_code=request.POST.get("preferredCourse"),
            preferred_section=preferred_section,
            preferred_faculty=preferred_faculty,
            preferred_time=preferred_time,
            preferred_days=preferred_days,

            # Any Options
            any_day=any_day,
            any_time=any_time,
            any_section=any_section,
            any_faculty=any_faculty
        )
        all_requests = SlotRequest.objects.filter(
          user__studentprofile__university=request.user.studentprofile.university,
          user__studentprofile__department=request.user.studentprofile.department
)         .exclude(user=request.user)

       # generate matches
        for other in all_requests:

            a_to_b, b_to_a, mutual = calculate_mutual_score(new_request, other)

            if a_to_b >= 60 and b_to_a >= 60:

                # avoid duplicates
                exists = Match.objects.filter(
                   Q(user_a=new_request.user, user_b=other.user) |
                   Q(user_a=other.user, user_b=new_request.user) 
                ).exists()

                if not exists:
                    Match.objects.create(
                        user_a=new_request.user,
                        user_b=other.user,

                        request_a=new_request,
                        request_b=other,

                        score_a_to_b=a_to_b,
                        score_b_to_a=b_to_a,
                        mutual_score=mutual
                    )

        return redirect("/my-requests/")

    return render(request, "create-request.html")

def forget_password_page(request):
    return render(request, "forget-password.html")

@login_required
def my_requests_page(request):
    user_requests = (
        SlotRequest.objects.filter(user=request.user)
        .order_by('-created_at')
    )

    return render(request, "my-requests.html", {
        "requests": user_requests
    })

@login_required
def delete_request(request, request_id):

    req = get_object_or_404(SlotRequest, id=request_id, user=request.user)
    req.delete()

    return redirect("/my-requests/")

@login_required
def delete_multiple(request):
    ids = request.GET.get("ids")

    if ids:
        ids_list = ids.split(",")

        SlotRequest.objects.filter(
            id__in=ids_list,
            user=request.user
        ).delete()

    return redirect("/my-requests/")

@login_required
def matches_list_page(request):
    matches = Match.objects.filter(
        Q(user_a=request.user) | Q(user_b=request.user)
    ).order_by("-mutual_score")

    return render(request, "matches.html", {
        "matches": matches
    })

@login_required
def match_detail_page(request, match_id):
    match = Match.objects.get(id=match_id)

    return render(request, "match-details.html", {
        "match": match
        })

def notifications_page(request):
    return render(request, "notifications.html")
def profile_page(request):
    return render(request, "profile.html")
