from django.shortcuts import render
import joblib
import pandas as pd
import os


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
            "Years at Company": request.POST.get("years_at_company"),
            "Job Role": request.POST.get("job_role"),
            "Monthly Income": request.POST.get("monthly_income"),
            "Work-Life Balance": request.POST.get("work_life_balance"),
            "Job Satisfaction": request.POST.get("job_satisfaction"),
            "Performance Rating": request.POST.get("performance_rating"),
            "Number of Promotions": request.POST.get("number_of_promotions"),
            "Overtime": request.POST.get("overtime"),
            "Distance from Home": request.POST.get("distance_from_home"),
            "Education Level": request.POST.get("education_level"),
            "Marital Status": request.POST.get("marital_status"),
            "Number of Dependents": request.POST.get("number_of_dependents"),
            "Job Level": request.POST.get("job_level"),
            "Company Size": request.POST.get("company_size"),
            "Company Tenure (In Months)": request.POST.get("company_tenure"),
            "Remote Work": request.POST.get("remote_work"),
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
        print("\n========== DEBUG ==========")
        print("Input after encoding:")
        print(input_df.to_string(index=False))

        print("\nPrediction:", prediction)

        print("Model classes:", model.classes_)

        print("Probabilities:", model.predict_proba(input_df)[0])

        print("===========================\n")

        if prediction == 0:
            prediction_text = "Likely to Leave"
        else:
            prediction_text = "Likely to Stay"

        probability = model.predict_proba(input_df)[0][0] * 100
        probability = round(float(probability),2)


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