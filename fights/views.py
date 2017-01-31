from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from fights.models import Fighter, Fight
from fights.serializers import FighterSerializer, FightSerializer


class FighterList(generics.ListAPIView):
    #queryset = Fighter.objects.all().order_by('name')
    serializer_class = FighterSerializer

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


class FightDetail(generics.RetrieveAPIView):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer


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
        context = super().get_context_data(**kwargs)
        context['fights'] = Fight.objects.count()
        context['fighters'] = Fighter.objects.count()
        return context

