# Generated by Django 4.2.4 on 2023-08-22 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="AskStory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.BigIntegerField(unique=True)),
                ("item_type", models.CharField(max_length=100)),
                ("by", models.CharField(max_length=50)),
                ("time", models.BigIntegerField()),
                ("descendants", models.IntegerField(default=0)),
                ("score", models.IntegerField(default=0)),
                ("title", models.CharField(max_length=256)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.BigIntegerField(unique=True)),
                ("item_type", models.CharField(max_length=100)),
                ("by", models.CharField(max_length=50)),
                ("time", models.BigIntegerField()),
                ("title", models.TextField()),
                ("url", models.URLField(blank=True)),
                ("text", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.BigIntegerField(unique=True)),
                ("item_type", models.CharField(max_length=100)),
                ("by", models.CharField(max_length=50)),
                ("time", models.BigIntegerField()),
                ("parts", models.TextField()),
                ("score", models.IntegerField(default=0)),
                ("text", models.TextField()),
                ("title", models.CharField(max_length=256)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Story",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.BigIntegerField(unique=True)),
                ("item_type", models.CharField(max_length=100)),
                ("by", models.CharField(max_length=50)),
                ("time", models.BigIntegerField()),
                ("descendants", models.IntegerField(default=0)),
                ("score", models.IntegerField(default=0)),
                ("title", models.CharField(max_length=256)),
                ("url", models.URLField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.BigIntegerField(unique=True)),
                ("item_type", models.CharField(max_length=100)),
                ("by", models.CharField(max_length=50)),
                ("time", models.BigIntegerField()),
                ("text", models.TextField()),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="app_comment_content_77122d_idx",
                    )
                ],
            },
        ),
    ]