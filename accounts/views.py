from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from resources.models import Resource
from resource_requests.models import Request

from .forms import LoginForm, RegisterForm


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "accounts/register.html", {"form": form})


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
