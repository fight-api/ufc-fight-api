from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy

from fights.forms import FighterQueryForm
from fights.models import Fighter, Fight, Event, FightQuery
from fights.serializers import FighterSerializer, FightSerializer, \
    EventSerializer, FighterListSerializer
import logging
import json

request_logger = logging.getLogger('main_page')


class ListPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class FighterList(generics.ListAPIView):
    serializer_class = FighterListSerializer
    pagination_class = ListPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            uppered = [x.capitalize() for x in name.split('_')]
            cleaned_name = ' '.join(uppered)
            qs = Fighter.objects.filter(name=cleaned_name).all()
            return qs
        else:
            return Fighter.objects.all().order_by('name')


class FighterDetail(generics.RetrieveAPIView):
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer


class FightList(generics.ListAPIView):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer
    filter_fields = ('id', 'round')


class FightDetail(generics.RetrieveAPIView):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RefereeSummary(APIView):

    def get(self, request, format=None):
        data = Fight.objects.values('referee').annotate(
            number=Count('pk')).order_by('-number')
        return Response(data)


class FinishSummary(APIView):
    def get(self, request, format=None):
        data = Fight.objects.values('method').annotate(
            number=Count('pk')).order_by('-number')

        return Response(data)


class IntroAPI(ListView):
    template_name = 'fights/intro_api.html'
    queryset = Fight.objects.all()

    def get_context_data(self, **kwargs):
        request_logger.debug(self.request.environ)

        context = super().get_context_data(**kwargs)
        context['fights'] = Fight.objects.count()
        context['fighters'] = Fighter.objects.count()
        context['events'] = Event.objects.count()

        fight = Fight.objects.get(id=2335)
        context['fight_ex'] = json.dumps(FightSerializer(fight).data, indent=4)
        return context


class DataExplorer(CreateView):
    model = FightQuery
    template_name = 'fights/data_explorer.html'
    form_class = FighterQueryForm
    success_url = reverse_lazy('data_results')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_searches'] = FightQuery.objects.order_by('-created_date')[:5]
        return context



def data_query(request):
    if request.method == 'POST':
        form = FighterQueryForm(request.POST)
        if form.is_valid():
            fight_query = form.save()
            return redirect('data_results', pk=fight_query.pk)


class DataResults(TemplateView):
    template_name = 'fights/data_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fight_query = get_object_or_404(FightQuery, pk=context['pk'])
        results = fight_query.calc_win_rate()
        context['name'] = str(fight_query)
        context['recent_searches'] = FightQuery.objects.order_by('-created_date')[:5]
        context = {
            **context,
            **results
        }

        return context



