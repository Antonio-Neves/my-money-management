from django.views.generic import CreateView
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import redirect

from transactions.forms import CreateTransactionForm


class CreateTransactionView(CreateView):
    template_name = 'create_transaction.html'
    form_class = CreateTransactionForm
    success_url = reverse_lazy('index')

    # def form_valid(self, form):
    #     # --- Get Form data --- #
    #
    #     transacao_metodo = form.cleaned_data['transacao_metodo']
    #     transacao_valor = form.cleaned_data['transacao_valor']
    #     transacao_entrada_saida = form.cleaned_data['transacao_entrada_saida']
    #
    #
    #     # --- Use transaction from django db for integrity --- #
    #     with transaction.atomic():
    #
    #         form.save()
    #
    #         # --- Update value in transaction type --- #
    #         transacao_metodo.metodo_transacao_saldo += transacao_valor
    #         transacao_metodo.save()
    #
    #     return redirect(self.success_url)
