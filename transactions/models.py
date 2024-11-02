from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.html import format_html


TRANSACAO_E_S_CHOICES = {
    'E': 'Entrada',
    'S': 'Saída'
}


class UserConnected(models.Model):
    user_connected = models.ForeignKey(
        get_user_model(), verbose_name='Usuário conectado', on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class AreaTransacao(UserConnected):
    area_transacao_id = models.BigAutoField(
        'ID - Área Transação', primary_key=True
    )
    area_transacao_nome = models.CharField(
        'Área de Transação', max_length=100, unique=True
    )

    class Meta:
        verbose_name = 'Área de transação'
        verbose_name_plural = 'Áreas de transação'
        ordering = ['area_transacao_nome']

    def __str__(self):
        return f'{self.area_transacao_nome}'

    def get_absolute_url(self):
        return reverse("area-transacao", kwargs={"pk": self.pk})


class TipoTransacao(UserConnected):
    tipo_transacao_id = models.BigAutoField(
        'ID - Tipo Transação', primary_key=True
    )
    tipo_transacao_nome = models.CharField(
        'Tipo de Transação', max_length=100, unique=True
    )

    class Meta:
        verbose_name = 'Tipo de transação'
        verbose_name_plural = 'Tipos de transação'
        ordering = ['tipo_transacao_nome']

    def __str__(self):
        return f'{self.tipo_transacao_nome}'

    def get_absolute_url(self):
        return reverse("tipo-transacao", kwargs={"pk": self.pk})


class MetodoTransacao(UserConnected):
    metodo_transacao_id = models.BigAutoField(
        'ID - Método Transação', primary_key=True
    )
    metodo_transacao_nome = models.CharField(
        'Método de Transação', max_length=100, unique=True
    )
    metodo_transacao_saldo = models.DecimalField(
        'Saldo',
        max_digits=8,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Método de transação'
        verbose_name_plural = 'Métodos de transação'
        ordering = ['metodo_transacao_nome']

    def __str__(self):
        return f'{self.metodo_transacao_nome}'

    def get_absolute_url(self):
        return reverse("metodo-transacao", kwargs={"pk": self.pk})


class Transacao(UserConnected):
    transacao_id = models.BigAutoField(
        'ID - Entrada', primary_key=True
    )
    transacao_data = models.DateField(
        'Data', auto_now=False, auto_now_add=False
    )
    transacao_area = models.ForeignKey(
        AreaTransacao,
        related_name='transacao_areatransacao',
        related_query_name='transacao_area_transacao',
        on_delete=models.PROTECT
    )
    transacao_descricao = models.CharField(
        'Descrição', max_length=100
    )
    transacao_valor = models.DecimalField(
        'Valor', max_digits=8, decimal_places=2
    )
    transacao_metodo = models.ForeignKey(
        MetodoTransacao,
        related_name='transacao_metodotransacao',
        related_query_name='transacao_metodo_transacao',
        on_delete=models.PROTECT
    )
    transacao_tipo = models.ForeignKey(
        TipoTransacao,
        related_name='transacao_tipotransacao',
        related_query_name='transacao_tipo_transacao',
        on_delete=models.PROTECT
    )
    transacao_destino = models.ForeignKey(
        MetodoTransacao,
        related_name='entrada_destinotransacao',
        related_query_name='entrada_destino_transacao',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    transacao_entrada_saida = models.CharField(
        'Entrada/Saida',
        max_length=100,
        choices=TRANSACAO_E_S_CHOICES,
        default='Saída'
    )

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transações'
        ordering = ['transacao_data', 'transacao_descricao']

    def __str__(self):
        return f'{self.transacao_descricao}'

    def get_absolute_url(self):
        return reverse("transacao", kwargs={"pk": self.pk})

    def colored_transacao_descricao(self):

        if self.transacao_tipo.__str__() == 'Extra':
            return format_html(
                f'<span style="color: #FF6B6B; margin: 0; padding: 0; font-size: 1rem;">{self.transacao_descricao}</span>'
            )
        else:
            return self.transacao_descricao

    colored_transacao_descricao.short_description = 'Descrição'
    colored_transacao_descricao.allow_tags = True
    colored_transacao_descricao.admin_order_field = 'transacao_descricao'

    def colored_transacao_tipo(self):

        if self.transacao_tipo.__str__() == 'Extra':
            return format_html(
                f'<span style="color: #FF6B6B; margin: 0; padding: 0; font-size: 1rem;">{self.transacao_tipo}</span>'
            )
        else:
            return self.transacao_tipo

    colored_transacao_tipo.short_description = "Tipo de Transação"
    colored_transacao_tipo.allow_tags = True
    colored_transacao_tipo.admin_order_field = 'transacao_tipo'
