from rest_framework import serializers
from app.models import Story, AskStory, Job, Comment, Poll


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"
        read_only_fields = ["api_id", "by", "descendants", "score"]


class AskStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AskStory
        fields = "__all__"
        read_only_fields = ["api_id", "by", "score"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["api_id", "by"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        # exclude = ['api_id', 'object_id', 'time']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = "__all__"
        read_only_fields = ["api_id", "by", "score", "parts"]
