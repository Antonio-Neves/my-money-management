from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


METODO_TRANSACAO_TIPO_CHOICES = {
    'E': 'Eletrônico',
    'F': 'Físico'
}


class UserConnected(models.Model):
    user_connected = models.ForeignKey(
        get_user_model(), verbose_name='Usuário conectado', on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class MetodoTransacao(UserConnected):
    metodo_transacao_id = models.BigAutoField(
        'ID - Método Transação', primary_key=True
    )
    metodo_transacao_nome = models.CharField(
        'Método de Transação', max_length=100
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


class AreaTransacao(UserConnected):
    area_transacao_id = models.BigAutoField(
        'ID - Área Transação', primary_key=True
    )
    area_transacao_nome = models.CharField(
        'Área de Transação', max_length=100
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
        'Tipo de Transação', max_length=100
    )

    class Meta:
        verbose_name = 'Tipo de transação'
        verbose_name_plural = 'Tipos de transação'
        ordering = ['tipo_transacao_nome']

    def __str__(self):
        return f'{self.tipo_transacao_nome}'

    def get_absolute_url(self):
        return reverse("tipo-transacao", kwargs={"pk": self.pk})


class Entrada(UserConnected):
    entrada_id = models.BigAutoField(
        'ID - Entrada', primary_key=True
    )
    entrada_data = models.DateField(
        'Data', auto_now=False, auto_now_add=False
    )
    entrada_area = models.ForeignKey(
        AreaTransacao,
        related_name='entrada_areatransacao',
        related_query_name='entrada_areatransacao',
        on_delete=models.PROTECT
    )
    entrada_ds = models.CharField(
        'Descrição', max_length=100
    )
    entrada_tipo = models.ForeignKey(
        TipoTransacao,
        related_name='entrada_tipotransacao',
        related_query_name='entrada_tipotransacao',
        on_delete=models.PROTECT
    )
    entrada_valor = models.DecimalField(
        'Valor', max_digits=7, decimal_places=2
    )
    entrada_metodo_transacao = models.ForeignKey(
        MetodoTransacao,
        related_name='entrada_metodotransacao',
        related_query_name='entrada_metodotransacao',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['entrada_data', 'entrada_ds']

    def __str__(self):
        return f'{self.entrada_ds}'

    def get_absolute_url(self):
        return reverse("entrada", kwargs={"pk": self.pk})


class Saida(UserConnected):
    saida_id = models.BigAutoField(
        'ID - Saída', primary_key=True
    )
    saida_data = models.DateField(
        'Data', auto_now=False, auto_now_add=False
    )
    saida_area = models.ForeignKey(
        AreaTransacao,
        related_name='saida_areatransacao',
        related_query_name='saida_areatransacao',
        on_delete=models.PROTECT
    )
    saida_ds = models.CharField(
        'Descrição', max_length=100
    )
    saida_tipo = models.ForeignKey(
        TipoTransacao,
        related_name='saida_tipotransacao',
        related_query_name='saida_tipotransacao',
        on_delete=models.PROTECT
    )
    saida_valor = models.DecimalField(
        'Valor', max_digits=7, decimal_places=2
    )
    saida_metodo_transacao = models.ForeignKey(
        MetodoTransacao,
        related_name='saida_metodotransacao',
        related_query_name='saida_metodotransacao',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Saída'
        verbose_name_plural = 'Saídas'
        ordering = ['saida_data', 'saida_ds']

    def __str__(self):
        return f'{self.saida_ds}'

    def get_absolute_url(self):
        return reverse("saida", kwargs={"pk": self.pk})
