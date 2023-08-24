from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Item(models.Model):
    STORY = "story"
    ASKSTORY = "story"
    COMMENT = "comment"
    POLL = "poll"
    JOB = "job"

    ITEM_TYPES = [
        (STORY, "story"),
        (ASKSTORY, "story"),
        (COMMENT, "comment"),
        (POLL, "poll"),
        (JOB, "job"),
    ]
    api_id = models.BigIntegerField(unique=True, blank=True)
    item_type = models.CharField(
        max_length=100, editable=False, blank=False, null=False, choices=ITEM_TYPES
    )
    by = models.CharField(max_length=50)
    time = models.BigIntegerField(blank=False, null=False, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item_type.title()} by {self.by.title()}"


class Comment(Item):
    text = models.TextField(blank=False, null=False)
    content_type = models.ForeignKey(
        ContentType, blank=False, on_delete=models.CASCADE, editable=False
    )
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey()

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]


class Story(Item):
    descendants = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    title = models.CharField(max_length=256, blank=False)
    url = models.URLField(blank=False)
    comments = GenericRelation(Comment)


class AskStory(Item):
    descendants = models.IntegerField(default=0, editable=False)
    score = models.IntegerField(default=0)
    title = models.CharField(max_length=256, blank=False)
    comments = GenericRelation(Comment)


class Job(Item):
    title = models.TextField(blank=False, null=False)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True, null=False)
    comments = GenericRelation(Comment)


class Poll(Item):
    parts = models.TextField()
    score = models.IntegerField(default=0)
    text = models.TextField(blank=True)
    title = models.CharField(max_length=256, blank=False)
    comments = GenericRelation(Comment)
