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
from django.conf.urls import url, include
from django.contrib import admin

from fights.views import FighterList, FighterDetail, FightList, \
   FightDetail, RefereeSummary, FinishSummary, IntroAPI, EventList, EventDetail, DataExplorer, DataResults

urlpatterns = [
    url(r'^api/fighter/$', FighterList.as_view(), name="fighter_list"),
    url(r'^api/fighter/(?P<pk>\d+)/$', FighterDetail.as_view(),
        name="fighter_detail"),
    url(r'^api/fight/$', FightList.as_view(), name="fight_list"),
    url(r'^api/fight/(?P<pk>\d+)/$', FightDetail.as_view(),
        name="fight_detail"),
    url(r'^api/refs/$', RefereeSummary.as_view(), name="referee_summary"),
    url(r'^api/finish/$', FinishSummary.as_view(), name="finish_summary"),
    url(r'^api/event/$', EventList.as_view(), name='event_list'),
    url(r'^api/event/(?P<pk>\d+)/$', EventDetail.as_view(), name='event_detail'),
    url(r'^explorer/$', DataExplorer.as_view(), name='data_explorer'),
    url(r'^results/$', DataResults.as_view(), name='data_results'),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^$', IntroAPI.as_view(), name='intro'),

]
