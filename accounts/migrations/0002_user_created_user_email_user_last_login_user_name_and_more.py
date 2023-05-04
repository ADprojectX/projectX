# Generated by Django 4.2.1 on 2023-05-04 05:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="surname",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=50),
        ),
    ]
