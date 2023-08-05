"""risefor lobbying URL Configuration"""

from django.contrib.auth import get_user_model
from django.conf.urls import url
from risefor_lobbying.views import RepresentativeViewSet, ActionViewSet, ConvergenceViewSet,TotalSubmission

User = get_user_model()

urlpatterns = [
    url(r'^elected-officials/', RepresentativeViewSet.urls()),
    url(r'^active-actions/', ActionViewSet.urls()),
    url(r'^convergent-actions/', ConvergenceViewSet.urls()),
    url(r'total-actions/', TotalSubmission.urls()),
]