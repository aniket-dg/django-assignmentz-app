# Generated by Django 3.1.7 on 2022-04-28 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '0001_initial'),
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
            ],
            options={
                'ordering': ['-assignment_no'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_assignment', models.IntegerField(default=0)),
                ('check_no', models.IntegerField(default=0)),
                ('uncheck_no', models.IntegerField(default=0)),
                ('remaining_student', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asssigned_course', models.ManyToManyField(blank=True, to='database.Course')),
            ],
        ),
    ]
