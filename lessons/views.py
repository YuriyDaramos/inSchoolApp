from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson
from .forms import LessonForm
from student_groups.models import StudentGroup
from datetime import datetime


@login_required
def add_lesson(request, group_id):
    group = get_object_or_404(StudentGroup, id=group_id)

    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, group=group)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.group = group
            lesson.teacher = group.teacher

            schedule = group.schedule
            selected_date = form.cleaned_data["date"]
            if isinstance(selected_date, str):
                selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

            weekday = selected_date.strftime("%A")

            if weekday in schedule:
                lesson.time = schedule[weekday]["start_time"]

            lesson.save()
            return redirect("group_detail", group_id=group.id)
    else:
        form = LessonForm(group=group)

    return render(request, "lessons/add_lesson.html", {"form": form, "group": group})


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    group = lesson.group

    previous_lesson = Lesson.objects.filter(group=group, date__lt=lesson.date).order_by("-date", "-time").first()
    next_lesson = Lesson.objects.filter(group=group, date__gt=lesson.date).order_by("date", "time").first()

    is_admin = request.user.groups.filter(name="Administrators").exists()
    is_teacher = lesson.teacher == request.user or is_admin

    if request.method == 'POST' and is_teacher:
        new_status = request.POST.get('status')
        if new_status == 'conducted':
            lesson.is_conducted = True
        elif new_status == 'cancelled':
            lesson.is_conducted = False
        elif new_status == 'unset':
            lesson.is_conducted = None
        lesson.save()
        return redirect('lesson_detail', lesson_id=lesson.id)

    return render(request, "lessons/lesson_detail.html", {
        "lesson": lesson,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson,
        "is_admin": is_admin,
        "is_teacher": is_teacher,
    })


@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if not request.user.groups.filter(name="Administrators").exists():
        return redirect("home")

    group = lesson.group

    if request.method == "POST":
        if "delete" in request.POST:
            lesson.delete()
            return redirect("group_detail", group_id=group.id)

        form = LessonForm(request.POST, request.FILES, instance=lesson, group=group)
        if form.is_valid():
            form.save()
            return redirect("lesson_detail", lesson_id=lesson.id)
    else:
        form = LessonForm(instance=lesson, group=group)

    return render(request, "lessons/edit_lesson.html", {"form": form, "lesson": lesson})
