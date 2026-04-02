from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    semester = models.PositiveIntegerField()

    class Meta:
        unique_together = ("name", "department", "semester")
        ordering = ["department", "semester", "name"]

    def __str__(self):
        return f"{self.name} - Sem {self.semester}"

# Create your models here.
