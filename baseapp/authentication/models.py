from django.db import models
from django.contrib.auth.models import User

from authentication.utils.enums.level import Level
from authentication.utils.enums.vulnerability import Vulnerability


class Companie(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    is_tested = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - by: {self.created_by.username}"


class ReportVulnerability(models.Model):
    vulnerability = models.CharField(max_length=42)
    description = models.CharField(max_length=200)
    level = models.CharField(max_length=6)
    created_in = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    companie = models.ForeignKey(Companie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.vulnerability} in: {self.companie.name} by: {self.created_by.username}"
