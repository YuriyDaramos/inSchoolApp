from django.shortcuts import render
from courses.models import Course
from users.models import CustomUser


def home_view(request):
    teachers = CustomUser.objects.filter(groups__name="Teachers")
    courses = Course.objects.all()

    return render(request, "home.html", {
        "teachers": teachers,
        "courses": courses
    })
