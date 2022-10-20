from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import AddEmployeeAPI, CreateProfileAPI, ProfileAPI, ListOfPayrollsAPI, Logout, ListOfProfilesAPI, \
    PayrollsAPI

urlpatterns = [
    path("login/", obtain_auth_token),
    path("add_employee/", AddEmployeeAPI.as_view()),
    path("create_profile/<str:token>/", CreateProfileAPI.as_view(), name="create_profile"),
    path("profile/", ProfileAPI.as_view()),
    path("list_of_profiles/", ListOfProfilesAPI.as_view()),
    path("salaries/", PayrollsAPI.as_view()),
    path("list_of_salaries/", ListOfPayrollsAPI.as_view()),
    path("logout/", Logout.as_view())
]
