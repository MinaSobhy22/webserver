from django.conf.urls import url
from . import views

from views import AnalyzeAPI

app_name = 'analyze'

urlpatterns = [
    url(r'^$', AnalyzeAPI.as_view(), name='analyze'),
]
