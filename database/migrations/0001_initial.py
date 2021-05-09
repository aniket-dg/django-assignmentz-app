# Generated by Django 3.1.7 on 2021-05-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('course_code', models.BigIntegerField()),
                ('short_name', models.CharField(default='Initials', max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('term', models.CharField(max_length=10)),
            ],
        ),
    ]