# Generated by Django 3.1.7 on 2021-05-09 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerd_course', models.ManyToManyField(to='database.Course')),
                ('student_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment_Ans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_list', models.JSONField()),
                ('is_submitted', models.BooleanField(default=False)),
                ('is_checked', models.BooleanField(default=False)),
                ('marks_outof', models.CharField(default='Not Assigned yet!', max_length=30)),
                ('marks_obtained', models.CharField(default='0', max_length=30)),
                ('assignment_id', models.IntegerField(default=0)),
                ('course_id', models.ManyToManyField(to='database.Course')),
                ('student_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-assignment_id'],
            },
        ),
    ]
