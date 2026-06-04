from multiprocessing import context
from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from .models import SlotRequest, StudentProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import SlotRequest, Match
from .matching import calculate_mutual_score
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required
import random
from .models import RevealRequest
# Create your views here.

@login_required
def index(request):
    all_matches = Match.objects.filter(
        Q(user_a=request.user) | Q(user_b=request.user)
    )
    top_matches = all_matches.order_by("-mutual_score")[:4]
    total_matches = all_matches.count()

    successful_matches = 0
    for m in all_matches:
        reveal_a = RevealRequest.objects.filter(match=m, sender=m.user_a).first()
        reveal_b = RevealRequest.objects.filter(match=m, sender=m.user_b).first()
        if reveal_a and reveal_b and reveal_a.status == "accepted" and reveal_b.status == "accepted":
            successful_matches += 1

    active_requests = SlotRequest.objects.filter(user=request.user , status="Pending").count()

    success_rate = (
        (successful_matches / total_matches) * 100
        if total_matches > 0 else 0
    )
    insight = calculate_insight(request.user)

    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
 
    context = {
        "user": request.user,
        "matches": top_matches,
        "active_requests": active_requests,
        "total_matches": total_matches,
        "successful_matches": successful_matches,
        "overall_match": round(success_rate, 1),
        "insight": insight,
        "reveal_system_ready": True,
        "unread_notifications": unread_count,
    }

    return render( request, "index.html" , context)

def calculate_insight(user):
    matches = Match.objects.filter(
        Q(user_a=user) | Q(user_b=user)
    ).order_by("-mutual_score")

    if not matches.exists():
        return {"course": 0, "section": 0, "faculty": 0, "time": 0, "day": 0}

    top = matches.first()

    req_mine = top.request_a if top.user_a == user else top.request_b
    req_other = top.request_b if top.user_a == user else top.request_a

    def cat_score(category):
    
        if category == "course":
            val = 35 if req_mine.current_course_code == req_other.preferred_course_code else 0
            return round((val / 35) * 100)
        elif category == "section":
            if req_other.any_section:
                val = 16
            elif req_mine.current_section == req_other.preferred_section:
                val = 20
            else:
                val = 0
            return round((val / 20) * 100)
        elif category == "faculty":
            if req_other.any_faculty:
                val = 12
            elif req_mine.current_faculty == req_other.preferred_faculty:
                val = 15
            else:
                val = 0
            return round((val / 15) * 100)
        elif category == "time":
            if req_other.any_time:
                val = 12
            elif req_mine.current_time == req_other.preferred_time:
                val = 15
            else:
                val = 0
            return round((val / 15) * 100)
        elif category == "day":
            if req_other.any_day:
                val = 12
            else:
                days_mine = set((req_mine.current_days or "").split(","))
                days_other = set((req_other.preferred_days or "").split(","))
                overlap = days_mine & days_other
                if not days_other:
                    val = 12
                elif len(overlap) == len(days_other):
                    val = 15
                elif len(overlap) > 0:
                    val = 12
                else:
                    val = 0
            return round((val / 15) * 100)
        return 0

    return {
        "course": cat_score("course"),
        "section": cat_score("section"),
        "faculty": cat_score("faculty"),
        "time": cat_score("time"),
        "day": cat_score("day"),
    }

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        university = request.POST.get("university")
        department = request.POST.get("department")

        username = email.split('@')[0]
        entered_code = request.POST.get('verification_code')

        saved_code = request.session.get('verification_code')

        if entered_code != saved_code:
            messages.error(request,"Invalid verification code")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already registered! Please use another email."} )    
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
def send_verification_email(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email is required'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already registered'})
        code = random.randint(100000, 999999)
        request.session['verification_code'] = str(code)

        try:
            send_mail(
                'SlotMate Verification Code',
                f'Your SlotMate verification code is: {code}',
                'slotmateproject@gmail.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
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

                   Q(request_a=new_request, request_b=other) |
                   Q(request_a=other, request_b=new_request)

                ).exists()

                if not exists:
                    match = Match.objects.create(
                        user_a=new_request.user,
                        user_b=other.user,

                        request_a=new_request,
                        request_b=other,

                        score_a_to_b=a_to_b,
                        score_b_to_a=b_to_a,
                        mutual_score=mutual
                    )
                    Notification.objects.create(
                        user=other.user,
                        message=f"New match found: {new_request.current_course_code} ↔ {other.current_course_code}",
                        notification_type="match",
                        related_id=match.id
                    )

                    Notification.objects.create(
                        user=request.user,
                        message=f"You got a new match: {new_request.current_course_code}",
                        notification_type="match",
                        related_id=match.id
                    )
                
        return redirect("/my-requests/")
    return render(request, "create-request.html")

def forget_password_page(request):
    return render(request, "forget-password.html")

@login_required
def my_requests_page(request):
    status_filter = request.GET.get("status")
    query = SlotRequest.objects.filter(user=request.user)
    if status_filter:
        query = query.filter(status=status_filter)
    user_requests = query.order_by('-created_at')

    return render(request, "my-requests.html", {
        "requests": user_requests
    })

@login_required
def delete_request(request, request_id):

    req = get_object_or_404(SlotRequest, id=request_id, user=request.user)
    
    Match.objects.filter(
        Q(request_a=req) | Q(request_b=req)
    ).delete()
    
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
    match = get_object_or_404(Match, id=match_id)

    # current user er reveal request
    my_reveal = RevealRequest.objects.filter(
        match=match,
        sender=request.user
    ).first()

    # other user er reveal request
    other_reveal = RevealRequest.objects.filter(
        match=match,
        receiver=request.user
    ).first()
    if match.user_a == request.user:
       my_request = match.request_a
       their_request = match.request_b
    else:
       my_request = match.request_b
       their_request = match.request_a

    
    return render(request, "match-details.html", {
        "match": match,
        "my_request": my_request,
        "their_request": their_request,
        "my_reveal": my_reveal,
        "other_reveal": other_reveal,
    })

@login_required
def profile_page(request):
    user = request.user

    return render(request, "profile.html", {
        "user": user,
        "total_requests": SlotRequest.objects.filter(user=user).count(),
        "total_matches": Match.objects.filter(Q(user_a=user) | Q(user_b=user)).count(),
        "active_requests": SlotRequest.objects.filter(user=user, status="Pending").count(),
    })

@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        profile = user.studentprofile

        full_name = request.POST.get("full_name", "").split(" ", 1)

        user.first_name = full_name[0]

        if len(full_name) > 1:
            user.last_name = full_name[1]

        profile.university = request.POST.get("university")
        profile.department = request.POST.get("department")

        user.save()
        profile.save()

    return redirect("/profile/")
@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user

        old = request.POST.get("old_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if not user.check_password(old):
            messages.error(request, "Old password is incorrect")
            return redirect("/profile/")

        if new != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("/profile/")

        if len(new) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect("/profile/")

        user.set_password(new)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully")

    return redirect("/profile/")
def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")
    notifications.update(is_read=True)

    for n in notifications:
        if n.notification_type == "match" and n.related_id:
            n.link = f"/match/{n.related_id}/"
        elif n.notification_type in ["reveal_request", "reveal_accepted"] and n.related_id:
            n.link = f"/match/{n.related_id}/"
        else:
            n.link = None

    return render(request, "notification.html", {
        "notification": notifications
    })
@login_required
def send_reveal_request(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if match.user_a != request.user and match.user_b != request.user:
        return redirect("/matches/")

    if match.user_a == request.user:
        receiver = match.user_b
    else:
        receiver = match.user_a

    #already sent reveal request?
    already_exists = RevealRequest.objects.filter(
        match=match,
        sender=request.user
    ).exists()

    if not already_exists:
        reveal = RevealRequest.objects.create(
            match=match,
            sender=request.user,
            receiver=receiver,
            status="pending"
        )
        Notification.objects.create(
            user=receiver,
            message=f"Someone sent you a reveal request for match: {match.request_a.current_course_code} ↔ {match.request_b.current_course_code}",
            notification_type="reveal_request",
            related_id=match.id
        )

    return redirect(f"/match/{match.id}/")
@login_required
def accept_reveal(request, reveal_id):
    obj = get_object_or_404(RevealRequest, id=reveal_id)
    if obj.receiver == request.user:
        obj.status = "accepted"
        obj.save()

        
        match = obj.match
        reveal_a = RevealRequest.objects.filter(match=match, sender=match.user_a).first()
        reveal_b = RevealRequest.objects.filter(match=match, sender=match.user_b).first()

        both_accepted = (
            reveal_a and reveal_a.status == "accepted" and
            reveal_b and reveal_b.status == "accepted"
        )

        if both_accepted:
            Notification.objects.create(
                user=obj.sender,
                message="Both accepted! Identity is now revealed.",
                notification_type="reveal_accepted",
                related_id=match.id
            )
            Notification.objects.create(
                user=request.user,
                message="Both accepted! Identity is now revealed.",
                notification_type="reveal_accepted",
                related_id=match.id
            )
        else:
            
            Notification.objects.create(
                user=obj.sender,
                message="Your reveal request was accepted! Waiting for you to accept theirs.",
                notification_type="reveal_accepted",
                related_id=match.id
            )

    return redirect(f"/match/{obj.match.id}/")

@login_required
def reject_reveal(request, reveal_id):
    obj = get_object_or_404(RevealRequest, id=reveal_id)
    if obj.receiver == request.user:
        obj.status = "rejected"
        obj.save()
    return redirect(f"/match/{obj.match.id}/")
@login_required
def respond_reveal_request(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    reveal = RevealRequest.objects.filter(
        match=match,
        receiver=request.user
    ).first()

    if not reveal:
        return redirect(f"/match/{match.id}/")

    action = request.GET.get("action")

    if action == "accept":
        reveal.status = "accepted"
        reveal.save()
        Notification.objects.create(
            user=reveal.sender,
            message=f"Your reveal request was accepted! Click to see identity.",
            notification_type="reveal_accepted",
            related_id=match.id
        )
    elif action == "reject":
        reveal.status = "rejected"
        reveal.save()

    return redirect(f"/match/{match.id}/")
@login_required
def delete_notification(request, notification_id):
    notif = get_object_or_404(Notification, id=notification_id, user=request.user)
    notif.delete()
    return redirect("/notifications/")