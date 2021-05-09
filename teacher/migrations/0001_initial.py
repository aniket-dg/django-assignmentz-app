# Generated by Django 3.1.7 on 2021-05-09 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment_Q',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_no', models.IntegerField(default=0)),
                ('assignment_name', models.CharField(default='Title', max_length=50)),
                ('last_date', models.CharField(default='December 25, 2021', max_length=30)),
                ('question_list', models.JSONField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.course')),
            ],
            options={
                'ordering': ['-assignment_no'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asssigned_course', models.ManyToManyField(to='database.Course')),
                ('teacher_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_assignment', models.IntegerField(default=0)),
                ('check_no', models.IntegerField(default=0)),
                ('uncheck_no', models.IntegerField(default=0)),
                ('remaining_student', models.IntegerField(default=0)),
                ('assignment_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teacher.assignment_q')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.course')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='assignment_q',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher'),
        ),
    ]