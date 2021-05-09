from django.db import models

# Create your models here.

class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    course_code = models.BigIntegerField()
    short_name = models.CharField(max_length=10, default="Initials")
    name = models.CharField(max_length=100)
    term = models.CharField(max_length=10)
    def __str__(self):
        return u'%s' %(self.id)
