# Generated by Django 4.2.4 on 2024-01-15 21:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0019_alter_notification_students"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="start_date",
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]
