from django.urls import path
from .views import GenericNewsAPIView, ParentCommentAPIView

urlpatterns = [
    # path("story/",StoryAPIView.as_view(), name='story' ),
    path("<slug:item_type>/", GenericNewsAPIView.as_view(), name="news"),
    path(
        "<slug:parent_name>/<int:parent_id>/comment/",
        ParentCommentAPIView.as_view(),
        name="parent_comments",
    ),
]
