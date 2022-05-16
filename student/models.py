from django.db import models
from users.models import User
from database.models import Course
from teacher.models import Assignment_Q
# Create your models here.

class Student(models.Model):
    student_id = models.OneToOneField(User, on_delete= models.CASCADE)
    registerd_course = models.ManyToManyField(Course, blank=True)
    def __str__(self):
        return u'%s' %(self.student_id)
    
class Assignment_Ans(models.Model):
    answer_list = models.JSONField()
    is_submitted = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    marks_outof = models.CharField(max_length=30, default="Not Assigned yet!")
    marks_obtained = models.CharField(max_length=30, default="0")
    assignment_id = models.IntegerField(primary_key=False, default=0)
    course_id = models.ManyToManyField(Course)
    student_id = models.ManyToManyField(User)
    def __str__(self):
        return u'%s %s' %(self.student_id, self.assignment_id)
    class Meta:
        ordering = ['-assignment_id']