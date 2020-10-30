from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.conf import settings
import json

with open(settings.NEWS_JSON_PATH, "r") as json_file:
    news_items = json.load(json_file)


# Create your views here.
class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Coming soon")


class NewsView(View):
    def get_index(self, link):
        for i in range(len(news_items)):
            if news_items[i]["link"] == int(link):
                return i
        return None

    def get(self, request, link, *args, **kwargs):
        if self.get_index(link) is not None:
            context = {"news_dict_item": news_items[self.get_index(link)]}
            return render(request, "news/index.html", context=context)
