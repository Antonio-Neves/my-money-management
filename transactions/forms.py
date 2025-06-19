from django import forms

from transactions.models import Transacao


class CreateTransactionForm(forms.ModelForm):

    class Meta():
        model = Transacao

        fields = [
            'transacao_data',
            'transacao_area',
            'colored_transacao_descricao',
            'transacao_valor',
            'transacao_metodo',
            'colored_transacao_tipo',
            'transacao_destino',
            'transacao_entrada_saida'
        ]
