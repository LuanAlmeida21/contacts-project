# Generated by Django 4.2.2 on 2023-06-23 23:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=240)),
                ('description', models.TextField(blank=True)),
                ('created_contact', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
