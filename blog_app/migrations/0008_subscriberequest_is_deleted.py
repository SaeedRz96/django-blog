# Generated by Django 4.2.3 on 2023-07-29 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0007_subscriberequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriberequest',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
