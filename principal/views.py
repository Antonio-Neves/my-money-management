from django.shortcuts import render
from django.views.generic import TemplateView

months_list = [
	'Janeiro', 'Fevereiro', 'Março', 'abril',
	'maio', 'junho', 'julho', 'agosto',
	'setembro', 'outubro', 'novembro', 'dezembro'
]


# --- Home Page --- #
class IndexView(TemplateView):
	template_name = 'principal/index.html'
	extra_context = {'months_list': months_list}
