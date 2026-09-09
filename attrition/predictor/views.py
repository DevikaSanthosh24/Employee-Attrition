from django.shortcuts import render, redirect
from functools import wraps

import joblib
import pandas as pd
import os
import xgboost as xgb

from .models import Prediction


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "predictor",
    "model",
    "employee_attrition_xgb.json"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "predictor",
    "model",
    "employee_attrition_metadata.pkl"
)


# ============================================================
# LOAD XGBOOST MODEL
# ============================================================

model = xgb.XGBClassifier()

model.load_model(
    MODEL_PATH
)


# ============================================================
# LOAD MODEL METADATA
# ============================================================

model_data = joblib.load(
    METADATA_PATH
)

feature_names = model_data["feature_names"]

encoders = model_data["encoders"]

target_encoder = model_data.get(
    "target_encoder"
)


# ============================================================
# ADMIN ACCESS DECORATOR
# ============================================================

def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User is not logged in
        if not request.user.is_authenticated:

            return redirect("admin_login")


        # User is logged in but is not an admin/staff user
        if not request.user.is_staff:

            return redirect("admin_login")


        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


# ============================================================
# ADMIN LOGIN
# ============================================================

def admin_login(request):

    # Already logged in as admin
    if (
        request.user.is_authenticated
        and request.user.is_staff
    ):

        return redirect("dashboard")


    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        # Django authentication
        from django.contrib.auth import authenticate

        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            if user.is_staff:

                from django.contrib.auth import login

                login(
                    request,
                    user
                )

                return redirect(
                    "dashboard"
                )

            else:

                return render(
                    request,
                    "admin_login.html",
                    {
                        "error":
                        "You do not have administrator access."
                    }
                )

        else:

            return render(
                request,
                "admin_login.html",
                {
                    "error":
                    "Invalid username or password."
                }
            )


    return render(
        request,
        "admin_login.html"
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

def admin_logout(request):

    from django.contrib.auth import logout

    logout(request)

    return redirect(
        "admin_login"
    )


# ============================================================
# HOME PAGE
# ============================================================

@admin_required
def home(request):

    return render(
        request,
        "input.html"
    )


# ============================================================
# NORMALIZE TEXT VALUES
# ============================================================

def normalize_text(value):

    if value is None:

        return value


    value = str(value).strip()


    # Convert curly apostrophes
    value = value.replace(
        "’",
        "'"
    )

    value = value.replace(
        "‘",
        "'"
    )

    value = value.replace(
        "â€™",
        "'"
    )


    # Convert curly double quotes
    value = value.replace(
        "“",
        '"'
    )

    value = value.replace(
        "”",
        '"'
    )


    return value


# ============================================================
# PREDICTION
# ============================================================

@admin_required
def predict(request):

    if request.method != "POST":

        return render(
            request,
            "input.html"
        )


    # ========================================================
    # GET VALUES FROM FORM
    # ========================================================

    data = {

        "Age":
        request.POST.get("age"),

        "Gender":
        request.POST.get("gender"),

        "Years at Company":
        request.POST.get(
            "years_at_company"
        ),

        # ----------------------------------------------------
        # Industry is stored in job_role field
        # ----------------------------------------------------

        "Job Role":
        request.POST.get(
            "job_role"
        ),

        "Monthly Income":
        request.POST.get(
            "monthly_income"
        ),

        "Work-Life Balance":
        request.POST.get(
            "work_life_balance"
        ),

        "Job Satisfaction":
        request.POST.get(
            "job_satisfaction"
        ),

        "Performance Rating":
        request.POST.get(
            "performance_rating"
        ),

        "Number of Promotions":
        request.POST.get(
            "number_of_promotions"
        ),

        "Overtime":
        request.POST.get(
            "overtime"
        ),

        "Distance from Home":
        request.POST.get(
            "distance_from_home"
        ),

        "Education Level":
        request.POST.get(
            "education_level"
        ),

        "Marital Status":
        request.POST.get(
            "marital_status"
        ),

        "Number of Dependents":
        request.POST.get(
            "number_of_dependents"
        ),

        "Job Level":
        request.POST.get(
            "job_level"
        ),

        "Company Size":
        request.POST.get(
            "company_size"
        ),

        "Company Tenure (In Months)":
        request.POST.get(
            "company_tenure"
        ),

        "Remote Work":
        request.POST.get(
            "remote_work"
        ),

        "Leadership Opportunities":
        request.POST.get(
            "leadership_opportunities"
        ),

        "Innovation Opportunities":
        request.POST.get(
            "innovation_opportunities"
        ),

        "Company Reputation":
        request.POST.get(
            "company_reputation"
        ),

        "Employee Recognition":
        request.POST.get(
            "employee_recognition"
        )
    }


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    input_df = pd.DataFrame(
        [data]
    )


    # ========================================================
    # NORMALIZE TEXT VALUES
    # ========================================================

    for column in input_df.columns:

        if input_df[column].dtype == "object":

            input_df[column] = (
                input_df[column]
                .apply(normalize_text)
            )


    # ========================================================
    # NUMERICAL FEATURES
    # ========================================================

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
            input_df[column],
            errors="coerce"
        )


    # ========================================================
    # CHECK INVALID NUMERICAL VALUES
    # ========================================================

    if (
        input_df[numeric_features]
        .isnull()
        .any()
        .any()
    ):

        return render(
            request,
            "input.html",
            {
                "error":
                "Please enter valid values for all numerical fields."
            }
        )


    # ========================================================
    # ENCODE CATEGORICAL FEATURES
    # ========================================================

    try:

        for column, encoder in encoders.items():

            if column in input_df.columns:

                input_df[column] = (
                    input_df[column]
                    .apply(normalize_text)
                )

                input_df[column] = (
                    encoder.transform(
                        input_df[column]
                    )
                )


    except ValueError as e:

        return render(
            request,
            "input.html",
            {
                "error":
                "Invalid value entered for one of the categorical fields: "
                + str(e)
            }
        )


    # ========================================================
    # ARRANGE FEATURES IN MODEL ORDER
    # ========================================================

    try:

        input_df = input_df[
            feature_names
        ]

    except KeyError as e:

        return render(
            request,
            "input.html",
            {
                "error":
                "Model feature mismatch: "
                + str(e)
            }
        )


    # ========================================================
    # MAKE PREDICTION
    # ========================================================

    try:

        prediction = model.predict(
            input_df
        )[0]

    except Exception as e:

        return render(
            request,
            "input.html",
            {
                "error":
                "Prediction error: "
                + str(e)
            }
        )


    # ========================================================
    # GET PROBABILITIES
    # ========================================================

    try:

        probabilities = model.predict_proba(
            input_df
        )[0]

    except Exception as e:

        return render(
            request,
            "input.html",
            {
                "error":
                "Probability calculation error: "
                + str(e)
            }
        )


    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print(
        "\n========== DEBUG =========="
    )

    print(
        "Input after encoding:"
    )

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

    print(
        "Probabilities:",
        probabilities
    )

    print(
        "Feature names:",
        feature_names
    )

    print(
        "===========================\n"
    )


    # ========================================================
    # CONVERT PREDICTION TO TEXT
    # ========================================================

    if prediction == 0:

        prediction_text = (
            "Employee likely to LEAVE"
        )

    else:

        prediction_text = (
            "Employee likely to STAY"
        )


    # ========================================================
    # CALCULATE LEAVE PROBABILITY
    # ========================================================

    if 0 in model.classes_:

        leave_index = list(
            model.classes_
        ).index(0)

        probability = (
            probabilities[
                leave_index
            ] * 100
        )

    else:

        probability = 0


    probability = round(
        float(probability),
        2
    )


    # ========================================================
    # DETERMINE RISK LEVEL
    # ========================================================

    if probability >= 60:

        risk = "High Risk"

    elif probability >= 30:

        risk = "Moderate Risk"

    else:

        risk = "Low Risk"


    # ========================================================
    # SAVE PREDICTION
    # ========================================================

    try:

        Prediction.objects.create(

            age=int(
                data["Age"]
            ),

            gender=normalize_text(
                data["Gender"]
            ),

            years_at_company=int(
                data["Years at Company"]
            ),

            job_role=normalize_text(
                data["Job Role"]
            ),

            monthly_income=float(
                data["Monthly Income"]
            ),

            work_life_balance=normalize_text(
                data["Work-Life Balance"]
            ),

            job_satisfaction=normalize_text(
                data["Job Satisfaction"]
            ),

            performance_rating=normalize_text(
                data["Performance Rating"]
            ),

            number_of_promotions=int(
                data["Number of Promotions"]
            ),

            overtime=normalize_text(
                data["Overtime"]
            ),

            distance_from_home=float(
                data["Distance from Home"]
            ),

            education_level=normalize_text(
                data["Education Level"]
            ),

            marital_status=normalize_text(
                data["Marital Status"]
            ),

            number_of_dependents=int(
                data["Number of Dependents"]
            ),

            job_level=normalize_text(
                data["Job Level"]
            ),

            company_size=normalize_text(
                data["Company Size"]
            ),

            company_tenure=int(
                data["Company Tenure (In Months)"]
            ),

            remote_work=normalize_text(
                data["Remote Work"]
            ),

            leadership_opportunities=normalize_text(
                data["Leadership Opportunities"]
            ),

            innovation_opportunities=normalize_text(
                data["Innovation Opportunities"]
            ),

            company_reputation=normalize_text(
                data["Company Reputation"]
            ),

            employee_recognition=normalize_text(
                data["Employee Recognition"]
            ),

            prediction=prediction_text,

            probability=probability,

            risk=risk
        )


    except Exception as e:

        return render(
            request,
            "input.html",
            {
                "error":
                "Could not save prediction: "
                + str(e)
            }
        )


    # ========================================================
    # RESULT PAGE
    # ========================================================

    return render(
        request,
        "result.html",
        {
            "risk": risk,

            "probability": probability,

            "prediction": prediction_text,
        }
    )


# ============================================================
# DASHBOARD
# ============================================================

@admin_required
def dashboard(request):

    # ========================================================
    # GET ALL PREDICTIONS
    # ========================================================

    predictions = Prediction.objects.all()


    # ========================================================
    # TOTAL PREDICTIONS
    # ========================================================

    total_predictions = predictions.count()


    # ========================================================
    # LEAVE COUNT
    # ========================================================

    leave_count = predictions.filter(
        prediction="Employee likely to LEAVE"
    ).count()


    # ========================================================
    # STAY COUNT
    # ========================================================

    stay_count = predictions.filter(
        prediction="Employee likely to STAY"
    ).count()


    # ========================================================
    # HIGH RISK COUNT
    # ========================================================

    high_risk_count = predictions.filter(
        risk="High Risk"
    ).count()


    # ========================================================
    # RECENT PREDICTIONS
    # ========================================================

    recent_predictions = (
        predictions
        .order_by("-created_at")[:10]
    )


    # ========================================================
    # SEND DATA TO DASHBOARD
    # ========================================================

    return render(
        request,
        "dashboard.html",
        {
            "total_predictions":
            total_predictions,

            "leave_count":
            leave_count,

            "stay_count":
            stay_count,

            "high_risk_count":
            high_risk_count,

            "recent_predictions":
            recent_predictions,
        }
    )


# ============================================================
# INDUSTRY-WISE PREDICTION
# ============================================================

@admin_required
def industry_predictions(request):

    # ========================================================
    # GET ALL PREDICTIONS
    # ========================================================

    predictions = Prediction.objects.all()


    # ========================================================
    # GET UNIQUE INDUSTRIES
    # ========================================================

    industries = (
        predictions
        .values_list(
            "job_role",
            flat=True
        )
        .distinct()
    )


    # ========================================================
    # CREATE INDUSTRY DATA
    # ========================================================

    industry_data = []


    for industry in industries:

        industry_records = predictions.filter(
            job_role=industry
        )


        # ----------------------------------------------------
        # TOTAL
        # ----------------------------------------------------

        total = industry_records.count()


        # ----------------------------------------------------
        # LEAVE
        # ----------------------------------------------------

        leave = industry_records.filter(
            prediction="Employee likely to LEAVE"
        ).count()


        # ----------------------------------------------------
        # STAY
        # ----------------------------------------------------

        stay = industry_records.filter(
            prediction="Employee likely to STAY"
        ).count()


        # ----------------------------------------------------
        # HIGH RISK
        # ----------------------------------------------------

        high_risk = industry_records.filter(
            risk="High Risk"
        ).count()


        # ----------------------------------------------------
        # MODERATE RISK
        # ----------------------------------------------------

        moderate_risk = industry_records.filter(
            risk="Moderate Risk"
        ).count()


        # ----------------------------------------------------
        # LOW RISK
        # ----------------------------------------------------

        low_risk = industry_records.filter(
            risk="Low Risk"
        ).count()


        # ----------------------------------------------------
        # ATTRITION RATE
        # ----------------------------------------------------

        if total > 0:

            attrition_rate = round(
                (leave / total) * 100,
                2
            )

        else:

            attrition_rate = 0


        # ----------------------------------------------------
        # STORE DATA
        # ----------------------------------------------------

        industry_data.append({

            "name":
            industry,

            "total":
            total,

            "leave":
            leave,

            "stay":
            stay,

            "attrition_rate":
            attrition_rate,

            "high_risk":
            high_risk,

            "moderate_risk":
            moderate_risk,

            "low_risk":
            low_risk,
        })


    # ========================================================
    # SORT INDUSTRIES ALPHABETICALLY
    # ========================================================

    industry_data = sorted(
        industry_data,
        key=lambda x: str(
            x["name"]
        ).lower()
    )


    # ========================================================
    # SEND DATA TO TEMPLATE
    # ========================================================

    return render(
        request,
        "industry.html",
        {
            "industry_data":
            industry_data
        }
    )