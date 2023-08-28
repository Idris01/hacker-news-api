from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.validators import DataError
from drf_multiple_model.views import FlatMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from app.models import Story, Comment, Poll, AskStory, Job
from .serializers import (
    StorySerializer,
    CommentSerializer,
    JobSerializer,
    PollSerializer,
    AskStorySerializer,
)
from datetime import datetime
from .utility import tokenize


item_map = dict(job=Job, story=Story, comment=Comment, askstory=AskStory, poll=Poll)

serializer_map = dict(
    job=JobSerializer,
    story=StorySerializer,
    comment=CommentSerializer,
    askstory=AskStorySerializer,
    poll=PollSerializer,
)


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 20


class LatestNewsListAPIView(FlatMultipleModelAPIView):
    add_model_type = False
    sorting_field = "-created_at"
    search_fields = ("title",)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitPagination
    news_query_map = [
        {
            "queryset": Story.objects.all(),
            "serializer_class": StorySerializer,
            "label": "story",
        },
        {
            "queryset": AskStory.objects.all(),
            "serializer_class": AskStorySerializer,
            "label": "askstory",
        },
        {"queryset": Job.objects.all(), "serializer_class": JobSerializer, "label": "job"},
        {
            "queryset": Poll.objects.all(),
            "serializer_class": PollSerializer,
            "label": "poll",
        },
    ]

    def get_querylist(self):
        filters = self.request.query_params.get("news_type", "").strip().split(",")

        if filters[0] != "":
            return [item for item in self.news_query_map if item["label"] in filters]

        return self.news_query_map


class GenericNewsAPIView(generics.ListCreateAPIView):

    lookup_url_kwarg = "news_type"

    item_map = item_map

    serializer_map = serializer_map

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
    item_map = item_map

    serializer_map = serializer_map

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


class NewsListAPIView(APIView):

    item_map = item_map
    serializer_map = serializer_map
    filter_name = "news_type"
    search_name = "search"

    def get(self, request, format=None):
        if request.query_params:
            params = request.query_params.get(self.filter_name)
            search = request.query_params.get(self.search_name)

            if not params and not search:
                return Response([])
            else:
                items_filtered = []
                if params:
                    params = params.split(",")
                    for item_name, item_class in item_map.items():
                        if item_name != "comment" and item_name in params:
                            items_filtered.extend(
                                self.serializer_map[item_name](
                                    item_class.objects.all(), many=True
                                ).data
                            )
                if items_filtered:  # this confirms that there is params
                    search_items = []
                    if not search:
                        return Response(items_filtered, status=status.HTTP_200_OK)
                    token = tokenize(search)

                    for filtered in items_filtered:
                        text = filtered.get("text", "")
                        title = filtered.get("title", "")
                        text_and_title = text.lower() + " " + title.lower()
                        if any(
                            ((tok.find(text_and_title) + text_and_title.find(tok)) > -2)
                            for tok in token
                        ):
                            search_items.append(filtered)
                    return Response(search_items, status=status.HTTP_200_OK)
                elif search:
                    search_items = []
                    token = tokenize(search)
                    for item_name, item_class in item_map.items():
                        if item_name != "comment":
                            items_filtered.extend(
                                self.serializer_map[item_name](
                                    item_class.objects.all(), many=True
                                ).data
                            )
                    for filtered in items_filtered:
                        text = filtered.get("text", "")
                        title = filtered.get("title", "")
                        text_and_title = text.lower() + " " + title.lower()

                        if any(
                            ((tok.find(text_and_title) + text_and_title.find(tok)) > -2)
                            for tok in token
                        ):
                            search_items.append(filtered)
                    return Response(search_items, status=status.HTTP_200_OK)

        all_data = []
        for item_name, item_class in self.item_map.items():
            if item_name != "comment":
                this_items = item_class.objects.all()
                this_serialized = self.serializer_map[item_name](this_items, many=True)
                all_data.extend(this_serialized.data)
        all_data.sort(
            key=lambda x: -(
                datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            )
        )
        return Response(all_data, status=status.HTTP_200_OK)


class StoryRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = "id"
    serializer_class = StorySerializer
    queryset = Story.objects.all()


class AskStoryRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = "id"
    serializer_class = AskStorySerializer
    queryset = AskStory.objects.all()


class PollRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = "id"
    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class JobRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = "id"
    serializer_class = JobSerializer
    queryset = Job.objects.all()
