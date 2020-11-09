from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import json, random
from datetime import datetime

with open(settings.NEWS_JSON_PATH, "r") as json_file:
    news_items = json.load(json_file)


# Create your views here.
class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse("Coming soon")
        return redirect('/news/')


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
    def cut_created(items):
        result = list()
        for item in items:
            result.append({"created": item["created"][:10], "text": item["text"],
                           "title": item["title"], "link": item["link"]})
        result.sort(key=get_created, reverse=True)
        return result

    def select_items_by_title(self, title):
        result = list()
        items = self.cut_created(news_items)
        for item in items:
            if title in item['title']:
                result.append(item)
        return result

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            q = request.GET.get('q')
            if q is None or q == '':
                context = {'news_items':  self.cut_created(news_items)}
                return render(request, "news/main.html", context=context)
            else:
                context = {'news_items':  self.select_items_by_title(q)}
                return render(request, "news/main.html", context=context)

    def post(self, request, *args, **kwargs):
        random.seed()
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if request.method == 'POST':
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
