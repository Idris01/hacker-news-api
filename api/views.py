from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.validators import DataError
from app.models import Story, Comment, Poll, AskStory, Job
from .serializers import (
    StorySerializer,
    CommentSerializer,
    JobSerializer,
    PollSerializer,
    AskStorySerializer,
)
from datetime import datetime


class GenericNewsAPIView(generics.ListCreateAPIView):

    lookup_url_kwarg = "item_type"

    item_map = dict(job=Job, story=Story, comment=Comment, askstory=AskStory, poll=Poll)

    serializer_map = dict(
        job=JobSerializer,
        story=StorySerializer,
        comment=CommentSerializer,
        askstory=AskStorySerializer,
        poll=PollSerializer,
    )

    def get_queryset(self):
        item_type = self.kwargs[self.lookup_url_kwarg]
        if item_type in self.item_map.keys():
            return self.item_map[item_type].objects.all()
        raise DataError("Item type not found")

    def get_serializer_class(self):
        return self.serializer_map[self.kwargs[self.lookup_url_kwarg]]

    def create(self, request, *args, **kwargs):
        item_type = kwargs[self.lookup_url_kwarg]
        if item_type not in self.item_map:
            return Response(
                {"message": f"Unknown type {item_type}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data
        data["by"] = str(request.user)
        data["api_id"] = -int(datetime.now().timestamp())

        serializer = self.serializer_map[item_type]
        serialized_data = serializer(data=data)
        new_item = ""
        if serialized_data.is_valid():
            try:
                if item_type == "askstory":
                    if not data["title"].lower().startswith("ask hn"):
                        data["title"] = "Ask HN: " + data["title"]
                    new_item = AskStory(
                        by=request.user,
                        title=data["title"],
                        api_id=data["api_id"],
                        item_type=item_type,
                    )
                    new_item.save()

                elif item_type == "story":
                    new_item = Story(
                        by=request.user,
                        url=data.get("url", ""),
                        title=data["title"],
                        score=data.get("score", 0),
                        api_id=data["api_id"],
                        item_type=item_type,
                    )
                    new_item.save()

                elif item_type == "job":
                    if (
                        data.get("url", "").strip() == ""
                        and data.get("title", "").strip() == ""
                    ):
                        return Response(
                            {"message": "Job should contain at least a url or text"}
                        )
                    new_item = Job(
                        by=request.user,
                        api_id=data["api_id"],
                        item_type=item_type,
                        url=data.get("url", ""),
                        title=data["title"],
                        text=data.get("text", ""),
                    )
                    new_item.save()

                elif item_type == "poll":
                    new_item = Poll(
                        by=request.user,
                        api_id=data["api_id"],
                        item_type=item_type,
                        title=data["title"],
                        text=data.get("text", ""),
                    )
                    new_item.save()

                else:
                    return Response(
                        {"message": f"Item of type {item_type} cannot be created"},
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    )
                return Response(serializer(new_item).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": f"Error: {e}"}, status.HTTP_400_BAD_REQUEST)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentCommentAPIView(APIView):
    item_map = dict(job=Job, story=Story, askstory=AskStory, poll=Poll)

    serializer_map = dict(
        job=JobSerializer,
        story=StorySerializer,
        askstory=AskStorySerializer,
        poll=PollSerializer,
    )

    def get(self, request, parent_name, parent_id, format=None):

        if parent_name not in self.item_map:
            return Response(
                {
                    "message": "name should be one of {}".format(
                        ",".join(list(self.item_map.keys()))
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        parent = self.item_map[parent_name].objects.filter(id=parent_id)

        if not parent:
            return Response(
                {"message": f"{parent_name.title()} with id {parent_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        parent = parent[0]
        children = Comment.objects.filter(object_id=parent.id)
        serialized_children = CommentSerializer(children, many=True)

        return Response(serialized_children.data)

    def post(self, request, parent_name, parent_id, format=None):
        data = request.data

        if parent_name not in self.item_map:
            return Response(
                {
                    "message": "name should be one of {}".format(
                        ",".join(list(self.item_map.keys()))
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        parent = self.item_map[parent_name].objects.filter(id=parent_id)

        if not parent:
            return Response(
                {"message": f"{parent_name.title()} with id {parent_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        parent = parent[0]
        data["api_id"] = -int(datetime.now().timestamp())
        data["parent"] = parent
        data["by"] = str(request.user)
        data["object_id"] = parent_id
        data["item_type"] = "comment"

        serialize_comment = CommentSerializer(data=data)

        if serialize_comment.is_valid():
            new_comment = Comment(
                parent=parent,
                by=request.user,
                api_id=data["api_id"],
                object_id=parent_id,
                text=data["text"],
                item_type=data["item_type"],
            )

            new_comment.save()
            return Response(
                CommentSerializer(new_comment).data, status=status.HTTP_201_CREATED
            )
        return Response(serialize_comment.errors, status.HTTP_400_BAD_REQUEST)
