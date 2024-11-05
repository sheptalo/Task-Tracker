# Generated by Django 5.1.3 on 2024-11-05 08:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField()),
                ('status', models.CharField(choices=[('1', 'Активен'), ('2', 'Архивирован')], max_length=50)),
                ('participates', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('avatar', models.ImageField(upload_to='')),
                ('role', models.CharField(choices=[('1', 'a'), ('2', 'b'), ('3', 'c')], max_length=50)),
                ('projects', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('worker', models.IntegerField()),
                ('status', models.CharField(choices=[('1', 'Grooming'), ('2', 'In progress'), ('3', 'Dev'), ('4', 'Done')], max_length=50)),
                ('priority', models.CharField(choices=[('1', 'Низкий'), ('2', 'Средний'), ('3', 'Высокий')], max_length=50)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField()),
                ('timeline', models.DurationField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
                ('tester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usermodel')),
            ],
        ),
    ]
