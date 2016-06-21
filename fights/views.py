from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

#from fights.models import Fighter, Fight
#from fights.serializers import FighterSerializer, FightSerializer
#
#
# class FighterListCreate(generics.ListCreateAPIView):
#     queryset = Fighter.objects.all()
#     serializer_class = FighterSerializer
#     #permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class FighterDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Fighter.objects.all()
#     serializer_class = FighterSerializer
#     #permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class FightListCreate(generics.ListCreateAPIView):
#     queryset = Fight.objects.all()
#     serializer_class = FightSerializer
#
#
# class FightDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Fight.objects.all()
#     serializer_class = FightSerializer
#
#
# class FighterByName(generics.ListAPIView):
#     """
#     Expects a full fighter name to be sent in as a query string with
#     underscores between words.
#
#     Example: fightername/?name=joe_smith
#     """
#
#     serializer_class = FightSerializer
#
#     def get_queryset(self):
#
#         name = self.request.query_params.get('name')
#
#         if name:
#             uppered = [x.capitalize() for x in name.split('_')]
#             cleaned_name = " ".join(uppered)
#             fighter = Fighter.objects.get(name=cleaned_name)
#             qs = Fight.objects.filter(fighter=fighter)
#             return qs.order_by("-date")
#         else:
#             return []
#
#
# class FightFilter(generics.ListAPIView):
#     serializer_class = FightSerializer
#
#     def get_queryset(self):
#         return super().get_queryset()
#
#
# class SearchPage(ListView):
#     template_name = "fights/search_page.html"
#     queryset = Fight.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["fights"] = Fight.objects.count()
#         context["fighters"] = Fighter.objects.count()
#         return context
#
