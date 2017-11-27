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
    max_page_size = 5000


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
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Fight.objects.values('referee').annotate(
            number=Count('pk')).order_by('-number')
        return Response(data)


class FinishSummary(APIView):
    permission_classes = (IsAuthenticated,)
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

        win_group = wins.order_by('winner_int_age').values('winner_int_age').annotate(w_count=Count('winner_int_age'))
        loss_group = losses.order_by('loser_int_age').values('loser_int_age').annotate(l_count=Count('loser_int_age'))

        loss_dict = {}
        for loss in loss_group:
            loss_dict[loss['loser_int_age']] = loss['l_count']

        x = []
        y = []
        y2 = []
        for group in win_group:
            age = group['winner_int_age']
            w_count = group['w_count']
            l_count = loss_dict.get(age)
            if l_count:
                x.append(age)
                y.append(w_count/(w_count + l_count))
                y2.append((w_count + l_count) / 1000)
        if x and y:

            trace1 = go.Scatter(
                x=x,
                y=y,
                marker={'color': 'red', 'symbol': 104, 'size': "10"},
                mode='lines',
                name='Win rate'
            )
            trace2 = go.Scatter(
                x=x,
                y=y2,
                fill='tozeroy',
                mode='none',
                name='fight count / 1000'
            )
            data=go.Data([trace1, trace2])
            layout=go.Layout(title="Win percentage by age", xaxis={'title':'Age'}, yaxis={'title':'Win %'})
            figure=go.Figure(data=data,layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')

            context['graph'] = div

        return context
