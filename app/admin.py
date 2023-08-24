from django.contrib import admin
from .models import Comment, Poll, Story, AskStory, Job


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    pass


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    pass


@admin.register(AskStory)
class AskStoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
