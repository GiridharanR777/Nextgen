from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pathlib import Path

from subjects.models import Subject


class Resource(models.Model):
    RESOURCE_TYPES = (
        ("notes", "Notes"),
        ("pyq", "PYQ"),
        ("book", "Book"),
    )

    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="resources")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    file = models.FileField(upload_to="resources/")
    type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    downloads = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def file_format(self):
        if not self.file:
            return "N/A"
        suffix = Path(self.file.name).suffix
        return suffix[1:].upper() if suffix else "N/A"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="ratings")
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "resource")

    def __str__(self):
        return f"{self.resource.title} - {self.value}"


class DownloadEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="download_events")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="download_events")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} downloaded {self.resource.title}"
