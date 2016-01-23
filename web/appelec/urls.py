from django.conf.urls import url
from django.views.generic.base import RedirectView

from appelec import views

urlpatterns = [
    url(r'^search/', views.search, name='search'),
    url(r'^programs/', views.programs, name='programs'),
    url(r'^page/(?P<page>.+)/', views.page, name='page'),
    url(r'^autocomplete/', views.autocomplete, name='autocomplete'),
    url(r'^$', RedirectView.as_view(pattern_name='search', permanent=False))
]
