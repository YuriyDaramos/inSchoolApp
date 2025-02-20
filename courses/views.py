from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Course
from .forms import CourseForm


def course_list(request):
    courses = Course.objects.all()
    is_admin = request.user.groups.filter(name="Administrators").exists()
    return render(request, "courses/course_list.html", {"courses": courses, "is_admin": is_admin})


@login_required
def create_course(request):
    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm()
    return render(request, "courses/create_course.html", {"form": form})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teachers = course.teachers.all()
    groups = course.groups.all()
    is_admin = request.user.groups.filter(name="Administrators").exists()

    return render(request, "courses/course_detail.html", {
        "course": course,
        "teachers": teachers,
        "groups": groups,
        "is_admin": is_admin
    })


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    if request.method == "POST":

        if "delete" in request.POST:
            course.groups.clear()
            course.delete()
            return redirect("course_list")

        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_detail", course_id=course.id)
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/edit_course.html", {"form": form, "course": course})
