from django.urls import path
from . import views


urlpatterns = [

    # ========================================================
    # HOME / NEW PREDICTION PAGE
    # ========================================================

    path(
        "",
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
    # ADMIN LOGIN
    # ========================================================

    path(
        "admin-login/",
        views.admin_login,
        name="admin_login"
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