from django.db import models
from django.urls import reverse


METODO_TRANSACAO_TIPO_CHOICES = {
    'E': 'Eletrônico',
    'F': 'Físico'
}


class MetodoTransacao(models.Model):
    metodo_transacao_id = models.BigAutoField(
        'ID - Método Transação', primary_key=True
    )
    metodo_transacao_nome = models.CharField(
        'Método de Transação', max_length=100, unique=True
    )
    metodo_transacao_tipo = models.CharField(
        'Tipo de transação', max_length=1,
        choices=METODO_TRANSACAO_TIPO_CHOICES
    )

    class Meta:
        verbose_name = 'Método de transação'
        verbose_name_plural = 'Métodos de transação'
        ordering = ['metodo_transacao_nome']

    def __str__(self):
        return f'{self.metodo_transacao_nome}'

    def get_absolute_url(self):
        return reverse("metodo-transacao", kwargs={"pk": self.pk})


class Entrada(models.Model):
    entrada_id = models.BigAutoField(
        'ID - Entrada', primary_key=True
    )
    entrada_data = models.DateField(
        'Data', auto_now=False, auto_now_add=False
    )
    entrada_ds = models.CharField(
        'Descrição', max_length=100
    )
    entrada_valor = models.DecimalField(
        'Valor', max_digits=7, decimal_places=2
    )
    entrada_metodo_transacao = models.ForeignKey(
        'MetodoTransacao', default='Dinheiro',
        on_delete=models.SET_DEFAULT
    )

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['entrada_data', 'entrada_id']

    def __str__(self):
        return f'{self.entrada_ds}'

    def get_absolute_url(self):
        return reverse("entrada", kwargs={"pk": self.pk})
