from django import forms


class AttritionForm(forms.Form):

    age = forms.IntegerField(
        label="Age",
        min_value=18,
        max_value=70
    )

    gender = forms.ChoiceField(
        label="Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ]
    )

    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[
            ("Single", "Single"),
            ("Married", "Married"),
            ("Divorced", "Divorced"),
        ]
    )

    department = forms.ChoiceField(
        label="Department",
        choices=[
            ("Sales", "Sales"),
            ("Research & Development", "Research & Development"),
            ("Human Resources", "Human Resources"),
        ]
    )

    job_role = forms.ChoiceField(
        label="Job Role",
        choices=[
            ("Sales Executive", "Sales Executive"),
            ("Research Scientist", "Research Scientist"),
            ("Laboratory Technician", "Laboratory Technician"),
            ("Manufacturing Director", "Manufacturing Director"),
            ("Healthcare Representative", "Healthcare Representative"),
            ("Manager", "Manager"),
            ("Sales Representative", "Sales Representative"),
            ("Research Director", "Research Director"),
            ("Human Resources", "Human Resources"),
        ]
    )

    job_level = forms.IntegerField(
        label="Job Level",
        min_value=1,
        max_value=5
    )

    monthly_income = forms.FloatField(
        label="Monthly Income",
        min_value=0
    )

    years_at_company = forms.IntegerField(
        label="Years at Company",
        min_value=0
    )

    years_in_current_role = forms.IntegerField(
        label="Years in Current Role",
        min_value=0
    )

    years_since_last_promotion = forms.IntegerField(
        label="Years Since Last Promotion",
        min_value=0
    )

    work_life_balance = forms.IntegerField(
        label="Work Life Balance",
        min_value=1,
        max_value=4
    )

    job_satisfaction = forms.IntegerField(
        label="Job Satisfaction",
        min_value=1,
        max_value=4
    )

    overtime = forms.ChoiceField(
        label="Overtime",
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ]
    )

    distance_from_home = forms.FloatField(
        label="Distance From Home",
        min_value=0
    )