from django.contrib import admin
from django.urls import path, include

from inSchoolApp.views import home_view
from users.views import search


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("users/", include("users.urls")),
    path("courses/", include("courses.urls")),
    path("group/", include("student_groups.urls")),
    path("lessons/", include("lessons.urls")),
    path("search/", search, name="search"),
]
