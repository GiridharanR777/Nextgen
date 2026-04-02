from django.conf import settings
from django.db import models


class Request(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")
    fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fulfilled", "-created_at"]

    def __str__(self):
        return self.title

# Create your models here.
