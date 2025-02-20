from django import forms
from .models import Lesson
from datetime import datetime, timedelta


class LessonForm(forms.ModelForm):
    date = forms.ChoiceField(label="Date", choices=[])
    time = forms.ChoiceField(
        label="Time",
        choices=[("", "— Use default schedule time —")] + [
            (f"{hour:02}:{minute:02}", f"{hour:02}:{minute:02}")
            for hour in range(8, 21) for minute in (0, 30)
        ],
        required=False
    )

    class Meta:
        model = Lesson
        fields = ["name", "date", "time", "description", "materials"]

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        if group:
            self.fields["date"].choices = self.get_available_dates(group)
            self.group = group

        if "instance" in kwargs and kwargs["instance"]:
            lesson = kwargs["instance"]
            if lesson.time:
                self.fields["time"].initial = lesson.time.strftime("%H:%M")

    def get_available_dates(self, group):
        """Генерирует 10 ближайших незанятых дат."""
        schedule = group.schedule
        existing_lessons = group.lessons.values_list("date", flat=True)

        today = datetime.today().date()
        available_dates = []
        days_of_week = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
            "Friday": 4, "Saturday": 5, "Sunday": 6
        }

        active_days = [days_of_week[day] for day in schedule.keys() if day in days_of_week]

        current_date = today
        while len(available_dates) < 10:
            if current_date.weekday() in active_days and current_date not in existing_lessons:
                available_dates.append((current_date.strftime("%Y-%m-%d"), current_date.strftime("%A, %d %B %Y")))
            current_date += timedelta(days=1)

        return available_dates

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if isinstance(date, str):  # Если дата в виде строки, конвертируем в объект date
            date = datetime.strptime(date, "%Y-%m-%d").date()
            cleaned_data["date"] = date  # Обновляем значение

        if not time:  # Если время не выбрано, берем из расписания группы
            group = self.group
            schedule = group.schedule
            weekday = date.strftime("%A")
            if weekday in schedule:
                cleaned_data["time"] = schedule[weekday]["start_time"]
            else:
                raise forms.ValidationError("Invalid date selection. No schedule available for this day.")

        return cleaned_data
