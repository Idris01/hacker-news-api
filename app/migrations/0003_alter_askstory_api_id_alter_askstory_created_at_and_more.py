# Generated by Django 4.2.4 on 2023-08-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_askstory_options_alter_job_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="askstory",
            name="api_id",
            field=models.BigIntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name="askstory",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="api_id",
            field=models.BigIntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="object_id",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="job",
            name="api_id",
            field=models.BigIntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="poll",
            name="api_id",
            field=models.BigIntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name="poll",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="story",
            name="api_id",
            field=models.BigIntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name="story",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
