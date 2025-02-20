from django.urls import path

from lessons.views import add_lesson
from .views import edit_group, group_detail, add_students_to_group

urlpatterns = [
    path("<int:group_id>/", group_detail, name="group_detail"),
    path("<int:group_id>/edit/", edit_group, name="edit_group"),
    path("<int:group_id>/add_lesson/", add_lesson, name="add_lesson"),
    path("<int:group_id>/add_students/", add_students_to_group, name="add_students_to_group"),
]
