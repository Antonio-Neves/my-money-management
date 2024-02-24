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
