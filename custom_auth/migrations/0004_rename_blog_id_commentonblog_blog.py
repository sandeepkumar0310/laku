# Generated by Django 5.0.6 on 2024-05-11 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_commentonblog_likeonblog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentonblog',
            old_name='blog_id',
            new_name='blog',
        ),
    ]
