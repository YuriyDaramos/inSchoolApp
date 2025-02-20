from django import forms
from .models import Course
from django.contrib.auth import get_user_model


class CourseForm(forms.ModelForm):
    teachers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(groups__name="Teachers"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Teachers"
    )

    class Meta:
        model = Course
        fields = ["name", "description", "image", "teachers"]
