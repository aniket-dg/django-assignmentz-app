from django.db import models
from database.models import Course


# Create your models here.
from users.models import User


class Teacher(models.Model):
    teacher_id = models.OneToOneField(User, on_delete=models.CASCADE)
    asssigned_course = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return u'%s' % self.teacher_id


class Assignment_Q(models.Model):

    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assignment_no = models.IntegerField(null=False, default=0)
    assignment_name = models.CharField(max_length=50, default="Title")
    last_date = models.CharField(max_length=30, default="December 25, 2021")
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_list = models.JSONField()

    def __str__(self):
        return u'%s %s' % (self.teacher_id, self.assignment_no)

    class Meta:
        ordering = ['-assignment_no']


class Status(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment_id = models.OneToOneField(Assignment_Q, on_delete=models.CASCADE)
    submitted_assignment = models.IntegerField(primary_key=False, default=0)
    check_no = models.IntegerField(primary_key=False, default=0)
    uncheck_no = models.IntegerField(primary_key=False, default=0)
    remaining_student = models.IntegerField(primary_key=False, default=0)

    def __str__(self):
        return str(self.assignment_id)
