from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, IntegerField, Q, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render


@login_required
def leaderboard_view(request):
    User = get_user_model()
    users = (
        User.objects.annotate(
            upload_count=Coalesce(Count("resources", distinct=True), Value(0), output_field=IntegerField()),
            download_count=Coalesce(Count("download_events", distinct=True), Value(0), output_field=IntegerField()),
            high_rating_count=Coalesce(
                Count("resources__ratings", filter=Q(resources__ratings__value__gte=4), distinct=True),
                Value(0),
                output_field=IntegerField(),
            ),
        )
        .annotate(points=F("upload_count") * 10 + F("download_count") + F("high_rating_count") * 5)
        .order_by("-points", "name")
    )
    return render(request, "leaderboard/leaderboard.html", {"users": users})

# Create your views here.
