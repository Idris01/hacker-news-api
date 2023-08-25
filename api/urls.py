from django.urls import path
from .views import GenericNewsAPIView, ParentCommentAPIView, LatestNewsListAPIView

urlpatterns = [
    path("latest/", LatestNewsListAPIView.as_view(), name="latest"),
    path("<slug:item_type>/", GenericNewsAPIView.as_view(), name="news"),
    path(
        "<slug:parent_name>/<int:parent_id>/comment/",
        ParentCommentAPIView.as_view(),
        name="parent_comments",
    ),
]
