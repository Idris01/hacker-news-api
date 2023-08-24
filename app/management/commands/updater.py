from django.core.management.base import BaseCommand
from itertools import islice
from app.models import Comment, AskStory, Job, Poll, Story
import json
import http.client


def do_update():

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"
    NEWS_SIZE = 200  # the size of new to fetch at once
    ALLOWED_CHILDREN = 10  # maximum allowed children for any parent

    def get_payload(conn, id, payload, parent):
        conn.request("GET", f"/v0/item/{id}.json?print=pretty", payload)
        comm_resp = json.loads(conn.getresponse().read().decode("utf-8"))
        return Comment(
            api_id=comm_resp["id"],
            item_type=comm_resp["type"],
            by=comm_resp.get("by", ""),
            time=comm_resp["time"],
            text=comm_resp.get("text", ""),
            parent=parent,
        )

    def batch_save(parent, child_list, batch_size=100):
        objs = (get_payload(conn, key, payload, parent) for key in child_list)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Comment.objects.bulk_create(batch, batch_size)

    conn.request("GET", "/v0/topstories.json?print=pretty", payload)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))[:NEWS_SIZE]

    for item in data:
        conn.request("GET", f"/v0/item/{item}.json?print=pretty", payload)

        resp = json.loads(conn.getresponse().read().decode("utf-8"))
        typ = resp["type"]

        try:
            if (
                typ == "story"
                and not Story.objects.filter(api_id=resp["id"])
                and not resp["title"].lower().startswith("ask hn")
            ):
                obj = Story.objects.create(
                    api_id=resp["id"],
                    item_type=typ,
                    by=resp["by"],
                    time=resp["time"],
                    descendants=resp["descendants"],
                    url=resp.get("url", ""),
                    title=resp.get("title", ""),
                    score=resp["score"],
                )
                obj.save()

                if "kids" in resp and resp["kids"]:
                    batch_save(obj, resp["kids"][:ALLOWED_CHILDREN])
            elif typ == "poll" and not Poll.objects.filter(api_id=resp["id"]):
                obj = Poll.objects.create(
                    api_id=resp["id"],
                    item_type=typ,
                    by=resp["by"],
                    text=resp["text"],
                    time=resp["time"],
                    descendants=resp["descendants"],
                    title=resp["title"],
                    score=resp["score"],
                )
                obj.save()

                if "kids" in resp and resp["kids"]:
                    batch_save(obj, resp["kids"][:ALLOWED_CHILDREN])

            elif typ == "job" and not Poll.objects.filter(api_id=resp["id"]):
                obj = Job.objects.create(
                    api_id=resp["id"],
                    item_type=typ,
                    by=resp["by"],
                    text=resp.get("text", ""),
                    time=resp["time"],
                    url=resp.get("url", ""),
                    title=resp["title"],
                )
                obj.save()

                if "kids" in resp and resp["kids"]:
                    batch_save(obj, resp["kids"][:ALLOWED_CHILDREN])

            elif (
                typ == "story"
                and resp["title"].lower().startswith("ask hn")
                and not AskStory.objects.filter(api_id=resp["id"])
            ):  # Ask HN story
                obj = AskStory.objects.create(
                    api_id=resp["id"],
                    item_type="askstory",
                    by=resp["by"],
                    time=resp["time"],
                    descendants=resp["descendants"],
                    title=resp["title"],
                    score=resp["score"],
                )
                obj.save()

                if "kids" in resp and resp["kids"]:
                    try:
                        batch_save(obj, resp["kids"][:ALLOWED_CHILDREN])
                    except Exception:
                        raise Exception("Inside AskStory")

        except Exception as e:
            raise Exception(e)


class Command(BaseCommand):
    help = "Update the database at given interval"

    def handle(self, *args, **options):
        try:
            do_update()
        except Exception as e:
            self.stdout.write(self.style.SUCCESS(f"Error {e}"))

        self.stdout.write(self.style.SUCCESS("database updated"))
