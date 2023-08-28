from django.urls import path
from .views import (
    GenericNewsAPIView,
    ParentCommentAPIView,
    LatestNewsListAPIView,
    StoryRetrieveAPIView,
    JobRetrieveAPIView,
    AskStoryRetrieveAPIView,
    PollRetrieveAPIView,
)

urlpatterns = [
    path("latest/", LatestNewsListAPIView.as_view(), name="latest"),
    path("<slug:news_type>/", GenericNewsAPIView.as_view(), name="news"),
    path("story/<int:id>/", StoryRetrieveAPIView.as_view(), name="story_news"),
    path("job/<int:id>/", JobRetrieveAPIView.as_view(), name="job_news"),
    path("askstory/<int:id>/", AskStoryRetrieveAPIView.as_view(), name="askstory_news"),
    path("poll/<int:id>/", PollRetrieveAPIView.as_view(), name="poll_news"),
    path(
        "<slug:parent_name>/<int:parent_id>/comment/",
        ParentCommentAPIView.as_view(),
        name="parent_comments",
    ),
]
