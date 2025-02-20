from django.contrib.auth import get_user_model
from django.db import models


class StudentGroup(models.Model):
    name = models.CharField("Group Name", max_length=100)
    schedule = models.JSONField("Schedule", help_text="Schedule in the format of days of the week and times")
    description = models.CharField("Description", max_length=150, blank=True, null=True)
    teacher = models.ForeignKey(get_user_model(), related_name="teaching_groups", on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(get_user_model(), related_name="student_groups")
    course = models.ForeignKey("courses.Course", related_name="student_groups_courses", on_delete=models.CASCADE)
    is_active = models.BooleanField("Is Active", default=True)

    def __str__(self):
        return self.name
