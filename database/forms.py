from django import forms

from database.models import Course


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'short_name', 'name', 'term']