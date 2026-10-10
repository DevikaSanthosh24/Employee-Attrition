from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "age",
        "job_role",
        "job_level",
        "monthly_income",
        "prediction",
        "probability",
        "risk",
        "created_at",
    )

    list_filter = (
        "prediction",
        "risk",
        "job_role",
        "job_level",
    )

    search_fields = (
        "job_role",
        "prediction",
        "risk",
    )

    ordering = (
        "-created_at",
    )