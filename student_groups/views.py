from django.shortcuts import render, get_object_or_404, redirect

from courses.models import Course
from lessons.models import Lesson
from users.models import CustomUser
from .forms import GroupForm, DAYS_OF_WEEK
from django.contrib.auth.decorators import login_required

from .models import StudentGroup


@login_required
def add_group(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            schedule = {}
            for day in DAYS_OF_WEEK:
                start_time = form.cleaned_data.get(f"{day[0].lower()}_start_time")
                duration = form.cleaned_data.get(f"{day[0].lower()}_duration")
                if start_time or duration:
                    schedule[day[0]] = {
                        "start_time": start_time,
                        "duration": duration,
                    }
            new_group = form.save(commit=False)
            new_group.schedule = schedule
            new_group.course = course
            new_group.save()
            new_group.courses.add(course)
            return redirect("course_detail", course_id=course.id)
    else:
        form = GroupForm()

    return render(request, "groups/add_group.html", {"form": form, "course": course})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(StudentGroup, id=group_id)
    teacher = group.teacher
    lessons = Lesson.objects.filter(group=group)

    upcoming_lessons = lessons.filter(is_conducted__isnull=True).order_by("date", "time")
    past_lessons = lessons.filter(is_conducted__isnull=False).order_by("date", "time")

    is_admin = request.user.groups.filter(name="Administrators").exists()

    return render(request, "groups/group_detail.html", {
        "group": group,
        "teacher": teacher,
        "upcoming_lessons": upcoming_lessons,
        "past_lessons": past_lessons,
        "is_admin": is_admin
    })


@login_required
def edit_group(request, group_id):
    group = get_object_or_404(StudentGroup, id=group_id)

    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    if request.method == "POST":

        if "delete" in request.POST:
            group.delete()
            return redirect("course_list")

        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("group_detail", group_id=group.id)
    else:
        form = GroupForm(instance=group)

    return render(request, "groups/edit_group.html", {"form": form, "group": group})


@login_required
def add_students_to_group(request, group_id):
    group = get_object_or_404(StudentGroup, id=group_id)

    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    students_not_in_group = CustomUser.objects.filter(groups__name="Students").exclude(student_groups__id=group_id)

    if "q" in request.GET:
        query = request.GET["q"]
        students_not_in_group = students_not_in_group.filter(last_name__icontains=query)

    if "add_student" in request.POST:
        student_id = request.POST.get("student_id")
        student = CustomUser.objects.get(id=student_id)
        group.students.add(student)
        return redirect("add_students_to_group", group_id=group.id)

    if "remove_student" in request.POST:
        student_id = request.POST.get("student_id")
        student = CustomUser.objects.get(id=student_id)
        group.students.remove(student)
        return redirect("add_students_to_group", group_id=group.id)

    return render(request, "groups/add_students_to_group.html", {
        "group": group,
        "students": students_not_in_group,
    })
