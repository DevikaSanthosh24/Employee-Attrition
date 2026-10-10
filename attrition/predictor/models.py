from django.db import models


class Prediction(models.Model):

    # Employee input details
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    years_at_company = models.IntegerField()
    job_role = models.CharField(max_length=50)
    monthly_income = models.FloatField()
    work_life_balance = models.CharField(max_length=30)
    job_satisfaction = models.CharField(max_length=30)
    performance_rating = models.CharField(max_length=30)
    number_of_promotions = models.IntegerField()
    overtime = models.CharField(max_length=10)
    distance_from_home = models.FloatField()
    education_level = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20)
    number_of_dependents = models.IntegerField()
    job_level = models.CharField(max_length=20)
    company_size = models.CharField(max_length=20)
    company_tenure = models.IntegerField()
    remote_work = models.CharField(max_length=10)
    leadership_opportunities = models.CharField(max_length=10)
    innovation_opportunities = models.CharField(max_length=10)
    company_reputation = models.CharField(max_length=30)
    employee_recognition = models.CharField(max_length=30)

    # Prediction output
    prediction = models.CharField(max_length=30)
    probability = models.FloatField()
    risk = models.CharField(max_length=20)

    # Date and time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} - {self.probability}%"