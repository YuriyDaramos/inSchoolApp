from django.contrib.auth import get_user_model
from django.db import models
from student_groups.models import StudentGroup


class Course(models.Model):
    name = models.CharField("Course Name", max_length=100)
    description = models.CharField("Description", max_length=150, blank=True, null=True)
    image = models.ImageField("Course Image", upload_to="course_images/", blank=True, null=True)
    groups = models.ManyToManyField(StudentGroup, related_name="courses")
    teachers = models.ManyToManyField(get_user_model(), related_name="courses_taught", blank=True)

    def __str__(self):
        return self.name
