from django.contrib.auth import get_user_model
from django.db import models
from courses.models import Course
from student_groups.models import StudentGroup


class Lesson(models.Model):
    name = models.CharField("Lesson Name", max_length=100)
    group = models.ForeignKey(StudentGroup, related_name="lessons", on_delete=models.CASCADE)
    teacher = models.ForeignKey(get_user_model(), related_name="lessons", on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    description = models.TextField("Description", blank=True, null=True)
    materials = models.FileField(upload_to="lesson_materials/", blank=True, null=True)
    is_conducted = models.BooleanField("Conducted", null=True, blank=True)

    def __str__(self):
        return self.name
