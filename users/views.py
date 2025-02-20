from calendar import monthrange

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from lessons.models import Lesson
from student_groups.models import StudentGroup
from users.forms import UserProfileForm, CustomUserCreationForm
from users.models import CustomUser


def user_register(request):
    """Регистрация пользователя и добавление в группу "Students"."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="Students")
            user.groups.add(group)
            login(request, user)
            return redirect("user_profile", user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    """Авторизация пользователя."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user_profile", user_id=user.id)
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def user_profile(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    user_groups = user_obj.groups.all()

    is_admin = 'Administrators' in [group.name for group in request.user.groups.all()]

    return render(request, 'users/profile.html', {
        'user_obj': user_obj,
        'user_groups': user_groups,
        'is_admin': is_admin,
    })


@login_required
def edit_profile(request):
    """Редактирование профиля текущего пользователя."""
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_profile", user_id=user.id)
    else:
        form = UserProfileForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def calendar(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    today = timezone.now()
    month = request.GET.get("month", today.month)
    year = request.GET.get("year", today.year)

    try:
        month = int(month)
        year = int(year)
    except ValueError:
        month = today.month
        year = today.year

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    num_days_in_month = monthrange(year, month)[1]

    days_in_month = list(range(1, num_days_in_month + 1))

    student_groups = StudentGroup.objects.filter(students=user, is_active=True)
    teacher_groups = StudentGroup.objects.filter(teacher=user, is_active=True)
    groups = student_groups | teacher_groups

    # Курсы -> группы -> уроки
    calendar_data = {}
    for group in groups:
        course = group.course
        if course not in calendar_data:
            calendar_data[course] = {}
        calendar_data[course][group] = Lesson.objects.filter(group=group, date__month=month, date__year=year)

    if not calendar_data:
        no_lessons_message = "No lessons available for the selected month."
    else:
        no_lessons_message = None

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_name = months[month - 1]

    return render(request, "calendar/calendar_month.html", {
        "user": user,
        "calendar_data": calendar_data,
        "days_in_month": days_in_month,
        "month": month,
        "month_name": month_name,
        "year": year,
        "no_lessons_message": no_lessons_message,
    })


@login_required
def search(request):
    query = request.GET.get("q", "").strip()
    teachers, students, groups = [], [], []

    if query:
        teachers = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query),
                                             groups__name="Teachers")
        students = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query),
                                             groups__name="Students")
        groups = StudentGroup.objects.filter(name__icontains=query)

    return render(request, "users/search.html", {
        "query": query,
        "teachers": teachers,
        "students": students,
        "groups": groups
    })
