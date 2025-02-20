from django.urls import path
from .views import edit_lesson, lesson_detail

urlpatterns = [
    path("<int:lesson_id>/", lesson_detail, name="lesson_detail"),
    path("<int:lesson_id>/edit_lesson/", edit_lesson, name="edit_lesson"),
]
