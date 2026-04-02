from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RequestForm
from .models import Request


@login_required
def requests_view(request):
    form = RequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        req = form.save(commit=False)
        req.created_by = request.user
        req.save()
        return redirect("requests")
    requests_list = Request.objects.select_related("created_by").all()
    return render(request, "requests/requests.html", {"form": form, "requests_list": requests_list})

# Create your views here.
