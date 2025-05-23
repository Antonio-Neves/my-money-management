from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from base.mixins.mixins import FilterUserConnected
from transactions.models import Transacao


months_list = [
    ('January', 'Janeiro'), ('February', 'Fevereiro'), ('March', 'Março'),
    ('April', 'Abril'), ('May', 'Maio'), ('June', 'Junho'),
    ('July', 'Julho'), ('August', 'Agosto'), ('September', 'Setembro'),
    ('October', 'Outubro'), ('November', 'Novembro'), ('December', 'Dezembro')
]


# --- Home Page --- #
# class IndexView(TemplateView):
# 	template_name = 'principal/index.html'
# 	extra_context = {'months_list': months_list}


class IndexView(FilterUserConnected, ListView):
    template_name = 'principal/index.html'
    extra_context = {'months_list': months_list}
    queryset = Transacao.objects.select_related(
        'user_connected',
        'transacao_area',
        'transacao_metodo',
        'transacao_tipo',
        'transacao_destino'
    )
