"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from news.views import BaseView, NewsView, MainView, ComingSoonView, CreateView

urlpatterns = [
    path('', ComingSoonView.as_view()),
    path('base/', BaseView.as_view()),
    path('news/', MainView.as_view()),
    path('news/create/', CreateView.as_view()),
    re_path('news/(?P<link>[^/]*)/?', NewsView.as_view()),
]
