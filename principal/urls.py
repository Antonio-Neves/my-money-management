from django.contrib import admin
from django.urls import path

from principal.views import IndexView


urlpatterns = [
	path('', IndexView.as_view(), name='index'),
]
