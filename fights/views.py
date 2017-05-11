from django.contrib.auth.decorators import login_required
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
from rest_framework.permissions import IsAuthenticated

from fights.forms import FighterQueryForm
from fights.models import Fighter, Fight, Event, FightQuery
from fights.serializers import FighterSerializer, FightSerializer, \
    EventSerializer, FighterListSerializer
import logging
import json

import plotly.offline as opy
import plotly.graph_objs as go

request_logger = logging.getLogger('main_page')


class ListPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class FighterList(generics.ListAPIView):
    serializer_class = FighterListSerializer
    pagination_class = ListPagination
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)


class FightList(generics.ListAPIView):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer
    filter_fields = ('id', 'round')
    permission_classes = (IsAuthenticated,)


class FightDetail(generics.RetrieveAPIView):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer
    permission_classes = (IsAuthenticated,)


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)


class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)


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
        context['recent_searches'] = FightQuery.objects.order_by('-updated_date')[:5]
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
        fight_query.search_count += 1
        fight_query.save()

        wins, losses = fight_query.get_wins_losses()
        wins_count = wins.count()
        loss_count = losses.count()
        results_average = dict()
        if wins or losses:
            win_rate = wins_count/(wins_count + loss_count)
            results_average = {
                    'wins': wins_count,
                    'losses': loss_count,
                    'win_rate': "{0:.0f}%".format(win_rate * 100),
                    'win_size': win_rate * 100
                }

        context['name'] = str(fight_query)
        context['recent_searches'] = FightQuery.objects.order_by('-updated_date')[:5]

        context = {
            **context,
            **results_average
        }
        x = [-2,0,4,6,7]
        y = [q**2-q+3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                            mode="lines",  name='1st Trace')

        data=go.Data([trace1])
        layout=go.Layout(title="Win percentage by age", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return context
