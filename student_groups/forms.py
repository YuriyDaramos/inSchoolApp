from django import forms
from student_groups.models import StudentGroup
from django.contrib.auth import get_user_model

DAYS_OF_WEEK = [
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
]

START_TIME_CHOICES = [
    ("", ""),
    ("08:00", "08:00"),
    ("08:30", "08:30"),
    ("09:00", "09:00"),
    ("09:30", "09:30"),
    ("10:00", "10:00"),
    ("10:30", "10:30"),
    ("11:00", "11:00"),
    ("11:30", "11:30"),
    ("12:00", "12:00"),
    ("12:30", "12:30"),
    ("13:00", "13:00"),
    ("13:30", "13:30"),
    ("14:00", "14:00"),
    ("14:30", "14:30"),
    ("15:00", "15:00"),
    ("15:30", "15:30"),
    ("16:00", "16:00"),
    ("16:30", "16:30"),
    ("17:00", "17:00"),
    ("17:30", "17:30"),
    ("18:00", "18:00"),
    ("18:30", "18:30"),
    ("19:00", "19:00"),
    ("19:30", "19:30"),
    ("20:00", "20:00"),
]

DURATION_CHOICES = [
    ("", ""),
    (30, "30 minutes"),
    (45, "45 minutes"),
    (60, "1 hour"),
    (90, "1 hour 30 minutes"),
    (120, "2 hours"),
]


class GroupForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(groups__name="Teachers"),  # Фильтрация по группе "Teachers"
        required=True,
        label="Select Teacher"
    )

    monday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Monday Start Time")
    monday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Monday Duration")

    tuesday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Tuesday Start Time")
    tuesday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Tuesday Duration")

    wednesday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Wednesday Start Time")
    wednesday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Wednesday Duration")

    thursday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Thursday Start Time")
    thursday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Thursday Duration")

    friday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Friday Start Time")
    friday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Friday Duration")

    saturday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Saturday Start Time")
    saturday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Saturday Duration")

    sunday_start_time = forms.ChoiceField(choices=START_TIME_CHOICES, required=False, label="Sunday Start Time")
    sunday_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=False, label="Sunday Duration")

    class Meta:
        model = StudentGroup
        fields = ["name", "teacher"]


class StudentSearchForm(forms.Form):
    query = forms.CharField(label="Search by Last Name", max_length=100)
