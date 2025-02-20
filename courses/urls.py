from django.urls import path

from student_groups.views import add_group
from .views import course_list, create_course, course_detail, edit_course

urlpatterns = [
    path("", course_list, name="course_list"),
    path("create/", create_course, name="create_course"),
    path("<int:course_id>/", course_detail, name="course_detail"),
    path("<int:course_id>/edit/", edit_course, name="edit_course"),
    path("<int:course_id>/add_group/", add_group, name="add_group"),
]
