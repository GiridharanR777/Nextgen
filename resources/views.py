from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from resource_requests.models import Request
from subjects.models import Subject

from .forms import RatingForm, ResourceUploadForm
from .models import DownloadEvent, Rating, Resource


@login_required
def resource_list_view(request):
    resources = Resource.objects.select_related("subject", "uploaded_by").all()
    subjects = Subject.objects.all()
    departments = Subject.objects.values_list("department", flat=True).distinct()
    semesters = Subject.objects.values_list("semester", flat=True).distinct()

    department = request.GET.get("department")
    semester = request.GET.get("semester")
    subject_id = request.GET.get("subject")
    resource_type = request.GET.get("type")
    search = request.GET.get("search")

    if department:
        resources = resources.filter(subject__department=department)
    if semester:
        resources = resources.filter(subject__semester=semester)
    if subject_id:
        resources = resources.filter(subject_id=subject_id)
    if resource_type:
        resources = resources.filter(type=resource_type)
    if search:
        resources = resources.filter(title__icontains=search)

    return render(
        request,
        "resources/resource_list.html",
        {
            "resources": resources,
            "subjects": subjects,
            "departments": departments,
            "semesters": semesters,
            "resource_types": Resource.RESOURCE_TYPES,
        },
    )


@login_required
def upload_resource_view(request):
    form = ResourceUploadForm(request.POST or None, request.FILES or None)
    request_id = request.GET.get("request_id")
    if request.method == "POST" and form.is_valid():
        resource = form.save(commit=False)
        resource.uploaded_by = request.user
        resource.save()
        if request_id:
            Request.objects.filter(id=request_id).update(fulfilled=True)
        messages.success(request, "Resource uploaded successfully.")
        return redirect("resources")
    return render(request, "resources/upload.html", {"form": form, "request_id": request_id})


@login_required
def resource_detail_view(request, pk):
    resource = get_object_or_404(Resource.objects.select_related("subject", "uploaded_by"), pk=pk)
    existing = Rating.objects.filter(user=request.user, resource=resource).first()
    form = RatingForm(request.POST or None, instance=existing)
    if request.method == "POST" and form.is_valid():
        rating = form.save(commit=False)
        rating.user = request.user
        rating.resource = resource
        rating.save()
        avg_value = resource.ratings.aggregate(avg=Avg("value"))["avg"] or 0
        resource.rating = round(avg_value, 2)
        resource.save(update_fields=["rating"])
        messages.success(request, "Rating submitted.")
        return redirect("resource_detail", pk=resource.pk)
    return render(request, "resources/resource_detail.html", {"resource": resource, "form": form})


@login_required
def download_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if not resource.file:
        raise Http404("File not found.")
    resource.downloads += 1
    resource.save(update_fields=["downloads"])
    DownloadEvent.objects.create(user=request.user, resource=resource)
    return FileResponse(resource.file.open("rb"), as_attachment=True, filename=resource.file.name.split("/")[-1])

# Create your views here.
