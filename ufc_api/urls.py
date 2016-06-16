"""ufc_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from fights.views import FighterListCreate, FighterDetail, FightListCreate, \
    FightDetail, FighterByName, SearchPage

urlpatterns = [
    url(r'^fighter/$', FighterListCreate.as_view(), name="fighter_list"),
    url(r'^fighter/(?P<pk>\d+)/$', FighterDetail.as_view(),
        name="fighter_detail"),
    url(r'^fight/$', FightListCreate.as_view(), name="fight_list"),
    url(r'^fight/(?P<pk>\d+)/$', FightDetail.as_view(),
        name="fight_detail"),
    url(r'^fightername/$', FighterByName.as_view(), name="fighter_name"),
    url(r'^admin/', admin.site.urls),
    url(r'^$', SearchPage.as_view(), name="landing_page"),

]
