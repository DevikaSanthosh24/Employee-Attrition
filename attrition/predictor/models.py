from django.db import models


class Prediction(models.Model):

    # ============================================================
    # EMPLOYEE REFERENCE
    # ============================================================

    # Optional application-level identifier.
    # This is NOT used by the ML model.
    employee_reference = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


    # ============================================================
    # EMPLOYEE INPUT DETAILS
    # ============================================================

    age = models.IntegerField()

    gender = models.CharField(
        max_length=20
    )

    years_at_company = models.IntegerField()

    job_role = models.CharField(
        max_length=50
    )

    monthly_income = models.FloatField()

    work_life_balance = models.CharField(
        max_length=30
    )

    job_satisfaction = models.CharField(
        max_length=30
    )

    performance_rating = models.CharField(
        max_length=30
    )

    number_of_promotions = models.IntegerField()

    overtime = models.CharField(
        max_length=10
    )

    distance_from_home = models.FloatField()

    education_level = models.CharField(
        max_length=50
    )

    marital_status = models.CharField(
        max_length=20
    )

    number_of_dependents = models.IntegerField()

    job_level = models.CharField(
        max_length=20
    )

    company_size = models.CharField(
        max_length=20
    )

    company_tenure = models.IntegerField()

    remote_work = models.CharField(
        max_length=10
    )

    leadership_opportunities = models.CharField(
        max_length=10
    )

    innovation_opportunities = models.CharField(
        max_length=10
    )

    company_reputation = models.CharField(
        max_length=30
    )

    employee_recognition = models.CharField(
        max_length=30
    )


    # ============================================================
    # PREDICTION OUTPUT
    # ============================================================

    prediction = models.CharField(
        max_length=30
    )

    probability = models.FloatField()

    risk = models.CharField(
        max_length=20
    )


    # ============================================================
    # DATE AND TIME
    # ============================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # ============================================================
    # STRING REPRESENTATION
    # ============================================================

    def __str__(self):

        if self.employee_reference:

            return (
                f"{self.employee_reference} - "
                f"{self.prediction} - "
                f"{self.probability}%"
            )

        return (
            f"{self.prediction} - "
            f"{self.probability}%"
        )