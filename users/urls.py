from django.urls import path
from .views import user_register, user_login, user_logout, user_profile, edit_profile, calendar

urlpatterns = [
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/<int:user_id>/", user_profile, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("calendar/<int:user_id>/", calendar, name="calendar"),
]
