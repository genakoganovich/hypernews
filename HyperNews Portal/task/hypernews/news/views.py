from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
import json, random
from datetime import datetime

with open(settings.NEWS_JSON_PATH, "r") as json_file:
    news_items = json.load(json_file)


# Create your views here.
class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Coming soon")


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/base.html")


class NewsView(View):
    @staticmethod
    def get_index(link):
        for i in range(len(news_items)):
            if news_items[i]["link"] == int(link):
                return i
        return None

    def get(self, request, link, *args, **kwargs):
        if self.get_index(link) is not None:
            context = {"news_dict_item": news_items[self.get_index(link)]}
            return render(request, "news/index.html", context=context)


def get_created(e):
    return e["created"]


class MainView(View):
    @staticmethod
    def cut_created():
        result = list()
        for item in news_items:
            result.append({"created": item["created"][:10], "text": item["text"],
                           "title": item["title"], "link": item["link"]})
        result.sort(key=get_created, reverse=True)
        return result

    def get(self, request, *args, **kwargs):
        context = {'news_items': self.cut_created()}
        return render(request, "news/main.html", context=context)

    def post(self, request, *args, **kwargs):
        random.seed()
        now = datetime.now()
        created = now.strftime("%Y-%m-%d %H:%M:%S")
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = random.randint(4, 1000)
        news_items.append({"created": created, "text": text,
                           "title": title, "link": link})
        with open(settings.NEWS_JSON_PATH, "w") as json_f:
            json.dump(news_items, json_f)
        return redirect('/news/')


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html")
