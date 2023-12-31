# Generated by Django 4.2.4 on 2023-08-23 13:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="askstory",
            options={"ordering": ["-time"]},
        ),
        migrations.AlterModelOptions(
            name="job",
            options={"ordering": ["-time"]},
        ),
        migrations.AlterModelOptions(
            name="poll",
            options={"ordering": ["-time"]},
        ),
        migrations.AlterModelOptions(
            name="story",
            options={"ordering": ["-time"]},
        ),
        migrations.AddField(
            model_name="askstory",
            name="created_at",
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name="job",
            name="created_at",
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name="poll",
            name="created_at",
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name="story",
            name="created_at",
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name="askstory",
            name="descendants",
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name="askstory",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("story", "story"),
                    ("story", "story"),
                    ("comment", "comment"),
                    ("poll", "poll"),
                    ("job", "job"),
                ],
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="askstory",
            name="time",
            field=models.BigIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="comment",
            name="content_type",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("story", "story"),
                    ("story", "story"),
                    ("comment", "comment"),
                    ("poll", "poll"),
                    ("job", "job"),
                ],
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="object_id",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="comment",
            name="time",
            field=models.BigIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="job",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("story", "story"),
                    ("story", "story"),
                    ("comment", "comment"),
                    ("poll", "poll"),
                    ("job", "job"),
                ],
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="time",
            field=models.BigIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="poll",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("story", "story"),
                    ("story", "story"),
                    ("comment", "comment"),
                    ("poll", "poll"),
                    ("job", "job"),
                ],
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="poll",
            name="time",
            field=models.BigIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="story",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("story", "story"),
                    ("story", "story"),
                    ("comment", "comment"),
                    ("poll", "poll"),
                    ("job", "job"),
                ],
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="story",
            name="time",
            field=models.BigIntegerField(editable=False),
        ),
    ]
