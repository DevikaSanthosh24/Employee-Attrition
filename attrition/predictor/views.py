from django.shortcuts import render, redirect
from functools import wraps

import joblib
import pandas as pd
import os
import xgboost as xgb
import shap


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
# CREATE SHAP EXPLAINER
# ============================================================

try:

    shap_explainer = shap.TreeExplainer(
        model
    )

except Exception as e:

    shap_explainer = None

    print(
        "SHAP explainer could not be created:",
        str(e)
    )


# ============================================================
# ADMIN ACCESS DECORATOR
# ============================================================

def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            return redirect("admin_login")


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
# SHAP FEATURE INFORMATION
# ============================================================

# These are the features for which HR can reasonably
# consider an organisational action.

MODIFIABLE_FEATURES = {

    "Years at Company",

    "Monthly Income",

    "Work-Life Balance",

    "Job Satisfaction",

    "Performance Rating",

    "Number of Promotions",

    "Overtime",

    "Job Level",

    "Remote Work",

    "Leadership Opportunities",

    "Innovation Opportunities",

    "Employee Recognition",

}


# ============================================================
# HR ACTION SUGGESTIONS
# ============================================================

HR_ACTIONS = {

    "Years at Company":

        "Review long-term career development and growth opportunities.",


    "Monthly Income":

        "Review compensation and whether the employee's pay is aligned with the role and responsibilities.",


    "Work-Life Balance":

        "Review workload, working hours and work-life balance arrangements.",


    "Job Satisfaction":

        "Arrange a one-to-one discussion to understand workplace concerns and improve job satisfaction.",


    "Performance Rating":

        "Discuss performance feedback, development needs and suitable support.",


    "Number of Promotions":

        "Review career progression and whether appropriate promotion opportunities are available.",


    "Overtime":

        "Review overtime requirements and consider reducing excessive workload where possible.",


    "Job Level":

        "Review role responsibilities, career progression and opportunities for advancement.",


    "Remote Work":

        "Consider whether suitable remote or flexible working arrangements could improve the employee's work experience.",


    "Leadership Opportunities":

        "Consider providing suitable leadership responsibilities, mentoring or growth opportunities.",


    "Innovation Opportunities":

        "Provide opportunities for the employee to contribute ideas, projects and innovation initiatives.",


    "Employee Recognition":

        "Consider regular recognition, feedback and appreciation for the employee's contributions.",

}


# ============================================================
# CREATE SHAP-BASED HR ACTIONS
# ============================================================

def create_shap_actions(
    input_df,
    original_values,
    risk
):

    """
    Uses SHAP to identify the strongest model contributions.

    SHAP is used internally to identify which features have
    the strongest influence on the individual prediction.

    Only modifiable features are converted into HR actions.

    Non-modifiable attributes such as age, gender and marital
    status are intentionally excluded from suggested actions.
    """

    if shap_explainer is None:

        return []


    try:

        # ----------------------------------------------------
        # Calculate SHAP values
        # ----------------------------------------------------

        shap_values = shap_explainer.shap_values(
            input_df
        )


        # ----------------------------------------------------
        # Handle different SHAP output formats
        # ----------------------------------------------------

        if isinstance(
            shap_values,
            list
        ):

            if len(shap_values) == 0:

                return []

            leave_values = shap_values[0][0]

        else:

            shap_values = shap_values[0]

            leave_values = shap_values


        # ----------------------------------------------------
        # IMPORTANT
        #
        # The model uses:
        #
        # 0 = Leave
        # 1 = Stay
        #
        # SHAP contribution toward class 1 (Stay) is
        # converted into contribution toward Leave.
        # ----------------------------------------------------

        leave_contributions = -leave_values


        # ----------------------------------------------------
        # Build feature contribution list
        # ----------------------------------------------------

        feature_contributions = []


        for index, feature in enumerate(
            feature_names
        ):

            contribution = float(
                leave_contributions[index]
            )


            feature_contributions.append({

                "feature":
                feature,

                "contribution":
                contribution,

                "absolute":
                abs(contribution),

            })


        # ----------------------------------------------------
        # Sort by strongest contribution
        # ----------------------------------------------------

        feature_contributions.sort(
            key=lambda item:
            item["absolute"],
            reverse=True
        )


        # ----------------------------------------------------
        # Select only MODIFIABLE features
        # ----------------------------------------------------

        modifiable_contributions = [

            item

            for item in feature_contributions

            if item["feature"]
            in MODIFIABLE_FEATURES

        ]


        # ----------------------------------------------------
        # For High / Moderate risk:
        #
        # Prefer features contributing toward LEAVE.
        #
        # For Low risk:
        #
        # Prefer features contributing toward STAY,
        # so that HR can maintain those positive practices.
        # ----------------------------------------------------

        if risk in [
            "High Risk",
            "Moderate Risk"
        ]:

            relevant_features = [

                item

                for item
                in modifiable_contributions

                if item["contribution"] > 0

            ]

        else:

            relevant_features = [

                item

                for item
                in modifiable_contributions

                if item["contribution"] < 0

            ]


        # ----------------------------------------------------
        # If no directional features are available,
        # use the strongest modifiable features.
        # ----------------------------------------------------

        if not relevant_features:

            relevant_features = (
                modifiable_contributions
            )


        # ----------------------------------------------------
        # Create HR actions
        # ----------------------------------------------------

        actions = []

        used_features = set()


        for item in relevant_features:

            feature = item["feature"]


            if feature in used_features:

                continue


            if feature not in HR_ACTIONS:

                continue


            actions.append({

                "feature":
                feature,

                "action":
                HR_ACTIONS[feature],

                "value":
                original_values.get(
                    feature,
                    ""
                ),

                "direction":
                (
                    "risk"
                    if item["contribution"] > 0
                    else "protective"
                ),

            })


            used_features.add(
                feature
            )


            # Show a maximum of 4 actions

            if len(actions) >= 4:

                break


        return actions


    except Exception as e:

        print(
            "\n========== SHAP ACTION ERROR =========="
        )

        print(
            str(e)
        )

        print(
            "=======================================\n"
        )

        return []


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
    # GET EMPLOYEE REFERENCE
    # ========================================================

    employee_reference = normalize_text(
        request.POST.get(
            "employee_reference"
        )
    )


    if employee_reference == "":

        employee_reference = None


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
    # SAVE ORIGINAL HUMAN-READABLE VALUES
    #
    # These values are kept before categorical encoding.
    # They are used for displaying HR suggestions.
    # ========================================================

    original_values = {

        column:
        normalize_text(value)

        for column, value
        in data.items()

    }


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
        "Employee Reference:",
        employee_reference
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
    # CREATE SHAP-BASED HR ACTIONS
    # ========================================================

    suggested_actions = (
        create_shap_actions(
            input_df,
            original_values,
            risk
        )
    )


    # ========================================================
    # SAVE PREDICTION
    # ========================================================

    try:

        Prediction.objects.create(

            employee_reference=employee_reference,

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

            "risk":
            risk,

            "probability":
            probability,

            "prediction":
            prediction_text,

            "suggested_actions":
            suggested_actions,

        }
    )


# ============================================================
# DASHBOARD
# ============================================================

@admin_required
def dashboard(request):

    predictions = Prediction.objects.all()

    total_predictions = predictions.count()

    leave_count = predictions.filter(
        prediction="Employee likely to LEAVE"
    ).count()

    stay_count = predictions.filter(
        prediction="Employee likely to STAY"
    ).count()

    high_risk_count = predictions.filter(
        risk="High Risk"
    ).count()

    recent_predictions = (
        predictions
        .order_by("-created_at")[:10]
    )

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

    predictions = Prediction.objects.all()

    industries = (
        predictions
        .values_list(
            "job_role",
            flat=True
        )
        .distinct()
    )

    industry_data = []


    for industry in industries:

        industry_records = predictions.filter(
            job_role=industry
        )

        total = industry_records.count()

        leave = industry_records.filter(
            prediction="Employee likely to LEAVE"
        ).count()

        stay = industry_records.filter(
            prediction="Employee likely to STAY"
        ).count()

        high_risk = industry_records.filter(
            risk="High Risk"
        ).count()

        moderate_risk = industry_records.filter(
            risk="Moderate Risk"
        ).count()

        low_risk = industry_records.filter(
            risk="Low Risk"
        ).count()


        if total > 0:

            attrition_rate = round(
                (leave / total) * 100,
                2
            )

        else:

            attrition_rate = 0


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


    industry_data = sorted(
        industry_data,
        key=lambda x:
        str(
            x["name"]
        ).lower()
    )


    return render(
        request,
        "industry.html",
        {
            "industry_data":
            industry_data
        }
    )


# ============================================================
# OPENING PAGE
# ============================================================

def opening(request):

    return render(
        request,
        "opening.html"
    )