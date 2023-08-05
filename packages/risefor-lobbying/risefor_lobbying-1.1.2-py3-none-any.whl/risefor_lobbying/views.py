from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.serializers import ValidationError
from rest_framework.response import Response

from djangoldp.views import LDPViewSet
from risefor_lobbying.models import ActionGroup, Representative, Organisation, HomePageElectedOfficals
from datetime import date,datetime


class RepresentativeViewSet(LDPViewSet):
     model=Representative

     def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).exclude(function__icontains="attache")


class ActionViewSet(LDPViewSet):
     model=ActionGroup

     def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).exclude(actiondate__lt=date.today())


class OrganisationViewSet(LDPViewSet):
     model=Organisation

     def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).exclude(actiondate__lt=date.today())


class ConvergenceViewSet(LDPViewSet):
    '''
    ViewSet using Actions between two parameterised dates. If only one date is passed then
    only one is applied, i.e. if you pass start_date without end_date it will return all
    Actions after the start_date
    '''
    model=ActionGroup

    def get_queryset(self, *args, **kwargs):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = super().get_queryset(*args, **kwargs)

        if start_date is not None:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError('start_date was in an invalid format. Should be YYYY-MM-DD')
            queryset = queryset.filter(actiondate__gt=start_date)

        if end_date is not None:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError('end_date was in an invalid format. Should be YYYY-MM-DD')
            queryset = queryset.filter(actiondate__lt=end_date)

        return queryset

#view created to improve loading time of total messages sent on HP
class TotalSubmission(LDPViewSet):
    model = HomePageElectedOfficals
    
    def get_queryset(self, *args, **kwargs):
        allEmailsSent = HomePageElectedOfficals.objects.all()
        return allEmailsSent

    def list(self, request, *args, **kwargs):
        return Response({'total': self.get_queryset().count()})