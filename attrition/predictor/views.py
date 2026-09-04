from django.shortcuts import render
import joblib
import pandas as pd
import os
from .models import Prediction


# --------------------------------
# BASE DIRECTORY
# --------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# --------------------------------
# MODEL PATH
# --------------------------------

MODEL_PATH = os.path.join(
    BASE_DIR,
    "predictor",
    "model",
    "employee_attrition_model.pkl"
)


# --------------------------------
# LOAD SAVED MODEL
# --------------------------------

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
feature_names = model_data["feature_names"]
encoders = model_data["encoders"]


# --------------------------------
# HOME PAGE
# --------------------------------

def home(request):

    return render(
        request,
        "input.html"
    )


# --------------------------------
# PREDICTION
# --------------------------------

def predict(request):

    if request.method == "POST":

        # --------------------------------
        # GET VALUES FROM FORM
        # --------------------------------

        data = {
            "Age": request.POST.get("age"),
            "Gender": request.POST.get("gender"),
            "Years at Company": request.POST.get(
                "years_at_company"
            ),
            "Job Role": request.POST.get(
                "job_role"
            ),
            "Monthly Income": request.POST.get(
                "monthly_income"
            ),
            "Work-Life Balance": request.POST.get(
                "work_life_balance"
            ),
            "Job Satisfaction": request.POST.get(
                "job_satisfaction"
            ),
            "Performance Rating": request.POST.get(
                "performance_rating"
            ),
            "Number of Promotions": request.POST.get(
                "number_of_promotions"
            ),
            "Overtime": request.POST.get(
                "overtime"
            ),
            "Distance from Home": request.POST.get(
                "distance_from_home"
            ),
            "Education Level": request.POST.get(
                "education_level"
            ),
            "Marital Status": request.POST.get(
                "marital_status"
            ),
            "Number of Dependents": request.POST.get(
                "number_of_dependents"
            ),
            "Job Level": request.POST.get(
                "job_level"
            ),
            "Company Size": request.POST.get(
                "company_size"
            ),
            "Company Tenure (In Months)": request.POST.get(
                "company_tenure"
            ),
            "Remote Work": request.POST.get(
                "remote_work"
            ),
            "Leadership Opportunities": request.POST.get(
                "leadership_opportunities"
            ),
            "Innovation Opportunities": request.POST.get(
                "innovation_opportunities"
            ),
            "Company Reputation": request.POST.get(
                "company_reputation"
            ),
            "Employee Recognition": request.POST.get(
                "employee_recognition"
            )
        }


        # --------------------------------
        # CREATE DATAFRAME
        # --------------------------------

        input_df = pd.DataFrame([data])


        # --------------------------------
        # CONVERT NUMERICAL FEATURES
        # --------------------------------

        numeric_features = [
            "Age",
            "Years at Company",
            "Monthly Income",
            "Number of Promotions",
            "Distance from Home",
            "Number of Dependents",
            "Company Tenure (In Months)"
        ]

        for column in numeric_features:

            input_df[column] = pd.to_numeric(
                input_df[column]
            )


        # --------------------------------
        # ENCODE CATEGORICAL FEATURES
        # --------------------------------

        for column, encoder in encoders.items():

            if column in input_df.columns:

                input_df[column] = encoder.transform(
                    input_df[column]
                )


        # --------------------------------
        # ARRANGE FEATURES
        # --------------------------------

        input_df = input_df[feature_names]


        # --------------------------------
        # MAKE PREDICTION
        # --------------------------------

        prediction = model.predict(input_df)[0]


        # --------------------------------
        # DEBUG INFORMATION
        # --------------------------------

        print("\n========== DEBUG ==========")

        print("Input after encoding:")

        print(
            input_df.to_string(
                index=False
            )
        )

        print(
            "\nPrediction:",
            prediction
        )

        print(
            "Model classes:",
            model.classes_
        )

        probabilities = model.predict_proba(
            input_df
        )[0]

        print(
            "Probabilities:",
            probabilities
        )

        print("===========================\n")


        # --------------------------------
        # CONVERT PREDICTION TO TEXT
        # --------------------------------
        #
        # Model mapping:
        # 0 = Leave
        # 1 = Stay
        #

        if prediction == 0:

            prediction_text = (
                "Employee likely to LEAVE"
            )

        else:

            prediction_text = (
                "Employee likely to STAY"
            )


        # --------------------------------
        # ATTRITION PROBABILITY
        # --------------------------------
        #
        # Class 0 = Leave
        # Therefore probabilities[0]
        # represents probability of leaving.
        #

        probability = (
            probabilities[0] * 100
        )

        probability = round(
            float(probability),
            2
        )


        # --------------------------------
        # DETERMINE RISK
        # --------------------------------

        if probability >= 60:

            risk = "High Risk"

        elif probability >= 30:

            risk = "Moderate Risk"

        else:

            risk = "Low Risk"


        # --------------------------------
        # SAVE INPUT + OUTPUT TO DATABASE
        # --------------------------------

        Prediction.objects.create(

            # --------------------------------
            # INPUT VALUES
            # --------------------------------

            age=int(
                data["Age"]
            ),

            gender=data["Gender"],

            years_at_company=int(
                data["Years at Company"]
            ),

            job_role=data["Job Role"],

            monthly_income=float(
                data["Monthly Income"]
            ),

            work_life_balance=data[
                "Work-Life Balance"
            ],

            job_satisfaction=data[
                "Job Satisfaction"
            ],

            performance_rating=data[
                "Performance Rating"
            ],

            number_of_promotions=int(
                data["Number of Promotions"]
            ),

            overtime=data[
                "Overtime"
            ],

            distance_from_home=float(
                data["Distance from Home"]
            ),

            education_level=data[
                "Education Level"
            ],

            marital_status=data[
                "Marital Status"
            ],

            number_of_dependents=int(
                data["Number of Dependents"]
            ),

            job_level=data[
                "Job Level"
            ],

            company_size=data[
                "Company Size"
            ],

            company_tenure=int(
                data["Company Tenure (In Months)"]
            ),

            remote_work=data[
                "Remote Work"
            ],

            leadership_opportunities=data[
                "Leadership Opportunities"
            ],

            innovation_opportunities=data[
                "Innovation Opportunities"
            ],

            company_reputation=data[
                "Company Reputation"
            ],

            employee_recognition=data[
                "Employee Recognition"
            ],


            # --------------------------------
            # OUTPUT VALUES
            # --------------------------------

            prediction=prediction_text,

            probability=probability,

            risk=risk
        )


        # --------------------------------
        # SEND RESULT TO result.html
        # --------------------------------

        return render(
            request,
            "result.html",
            {
                "risk": risk,

                "probability": probability,

                "prediction": prediction_text,
            }
        )


    # --------------------------------
    # IF NOT POST
    # --------------------------------

    return render(
        request,
        "input.html"
    )


# --------------------------------
# DASHBOARD
# --------------------------------

def dashboard(request):

    # --------------------------------
    # GET ALL SAVED PREDICTIONS
    # --------------------------------

    predictions = Prediction.objects.all()


    # --------------------------------
    # TOTAL PREDICTIONS
    # --------------------------------

    total_employees = predictions.count()


    # --------------------------------
    # LEAVE / STAY COUNTS
    # --------------------------------

    employees_leave = predictions.filter(
        prediction="Employee likely to LEAVE"
    ).count()

    employees_stay = predictions.filter(
        prediction="Employee likely to STAY"
    ).count()


    # --------------------------------
    # ATTRITION RATE
    # --------------------------------

    if total_employees > 0:

        attrition_rate = round(
            (
                employees_leave
                / total_employees
            ) * 100,
            2
        )

        leave_percentage = round(
            (
                employees_leave
                / total_employees
            ) * 100,
            2
        )

        stay_percentage = round(
            (
                employees_stay
                / total_employees
            ) * 100,
            2
        )

    else:

        attrition_rate = 0

        leave_percentage = 0

        stay_percentage = 0


    # --------------------------------
    # RISK COUNTS
    # --------------------------------

    low_risk = predictions.filter(
        risk="Low Risk"
    ).count()

    moderate_risk = predictions.filter(
        risk="Moderate Risk"
    ).count()

    high_risk = predictions.filter(
        risk="High Risk"
    ).count()


    # --------------------------------
    # TOTAL RISK RECORDS
    # --------------------------------

    total_risk = (
        low_risk
        + moderate_risk
        + high_risk
    )


    # --------------------------------
    # RISK PERCENTAGES
    # --------------------------------

    if total_risk > 0:

        low_percentage = round(
            (
                low_risk
                / total_risk
            ) * 100,
            2
        )

        moderate_percentage = round(
            (
                moderate_risk
                / total_risk
            ) * 100,
            2
        )

        high_percentage = round(
            (
                high_risk
                / total_risk
            ) * 100,
            2
        )

    else:

        low_percentage = 0

        moderate_percentage = 0

        high_percentage = 0


    # --------------------------------
    # RECENT PREDICTIONS
    # --------------------------------

    recent_predictions = predictions.order_by(
        "-created_at"
    )[:10]


    # --------------------------------
    # SEND DATA TO DASHBOARD
    # --------------------------------

    return render(
        request,
        "dashboard.html",
        {
            "total_employees": total_employees,

            "employees_leave": employees_leave,

            "employees_stay": employees_stay,

            "attrition_rate": attrition_rate,

            "leave_percentage": leave_percentage,

            "stay_percentage": stay_percentage,

            "low_risk": low_risk,

            "moderate_risk": moderate_risk,

            "high_risk": high_risk,

            "low_percentage": low_percentage,

            "moderate_percentage": moderate_percentage,

            "high_percentage": high_percentage,

            "recent_predictions": recent_predictions,
        }
    )

