from django.urls import path
from . import views


urlpatterns = [

    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    path(
        "",
        views.admin_login,
        name="admin_login"
    ),


    # ========================================================
    # NEW PREDICTION PAGE
    # ========================================================

    path(
        "new-prediction/",
        views.home,
        name="home"
    ),


    # ========================================================
    # PREDICTION
    # ========================================================

    path(
        "predict/",
        views.predict,
        name="predict"
    ),


    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # ========================================================
    # INDUSTRY-WISE PREDICTION
    # ========================================================

    path(
        "industry-predictions/",
        views.industry_predictions,
        name="industry_predictions"
    ),


    # ========================================================
    # LOGOUT
    # ========================================================

    path(
        "logout/",
        views.admin_logout,
        name="admin_logout"
    ),

]