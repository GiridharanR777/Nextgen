from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from resources.models import Resource
from resource_requests.models import Request

from .forms import LoginForm, RegisterForm

import random
import time
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email")

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        # Store in session
        request.session['register_data'] = form.cleaned_data
        request.session['otp'] = otp
        request.session['otp_time'] = time.time()

        # Send email
        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,  # ✅ IMPORTANT
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")

    return render(request, "accounts/register.html", {"form": form})

import time
from django.contrib.auth import login
from django.shortcuts import render, redirect

def verify_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        otp_time = request.session.get("otp_time")

        # 🔒 Check OTP expiry (5 minutes)
        if otp_time and time.time() - otp_time > 300:
            return render(request, "accounts/verify_otp.html", {
                "error": "OTP expired. Please register again."
            })

        # ✅ Check OTP match
        if entered_otp == session_otp:
            data = request.session.get("register_data")

            form = RegisterForm(data)
            if form.is_valid():
                user = form.save()
                login(request, user)

                # 🧹 Clean session
                request.session.pop("otp", None)
                request.session.pop("register_data", None)
                request.session.pop("otp_time", None)

                return redirect("dashboard")

        else:
            return render(request, "accounts/verify_otp.html", {
                "error": "Invalid OTP"
            })

    return render(request, "accounts/verify_otp.html")

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.cleaned_data["user"])
        return redirect("dashboard")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login")


@login_required
def dashboard_view(request):
    recent_uploads = Resource.objects.select_related("subject", "uploaded_by").order_by("-created_at")[:5]
    context = {
        "recent_uploads": recent_uploads,
        "my_uploads": Resource.objects.filter(uploaded_by=request.user).count(),
        "open_requests": Request.objects.filter(fulfilled=False).count(),
        "total_resources": Resource.objects.count(),
    }
    return render(request, "dashboard.html", context)

# Create your views here.
