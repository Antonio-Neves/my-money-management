from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.db import transaction



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


class MetodoTransacao(UserConnected):
    metodo_transacao_id = models.BigAutoField(
        'ID - Método Transação', primary_key=True
    )
    metodo_transacao_nome = models.CharField(
        'Método de Transação', max_length=100
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
        default='S'
    )

    class Meta:
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transações'
        ordering = ['transacao_data', 'transacao_descricao']

    def __str__(self):
        return f'{self.transacao_descricao}'

    def get_absolute_url(self):
        return reverse("transacao", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # Verificar se é uma nova transação
        is_creating = self.pk is None
        old_valor = None
        old_metodo = None
        old_destino = None
        old_entrada_saida = None

        # Se está editando, buscar os valores antigos
        if not is_creating:
            try:
                old_transaction = Transacao.objects.get(pk=self.pk)
                old_valor = old_transaction.transacao_valor
                old_metodo = old_transaction.transacao_metodo
                old_destino = old_transaction.transacao_destino
                old_entrada_saida = old_transaction.transacao_entrada_saida
            except Transacao.DoesNotExist:
                is_creating = True

        with transaction.atomic():
            # Salvar a transação
            super().save(*args, **kwargs)

            if is_creating:
                # Nova transação - apenas aplicar o valor
                self._aplicar_valor_saldo(
                    self.transacao_metodo,
                    self.transacao_valor,
                    self.transacao_entrada_saida,
                    operacao='adicionar'
                )

                # Se há destino (transferência)
                if self.transacao_destino:
                    self._aplicar_valor_saldo(
                        self.transacao_destino,
                        self.transacao_valor,
                        'Entrada',  # Destino sempre recebe
                        operacao='adicionar'
                    )
            else:
                # Editando transação - reverter valores antigos e aplicar novos

                # Reverter valor antigo
                self._aplicar_valor_saldo(
                    old_metodo,
                    old_valor,
                    old_entrada_saida,
                    operacao='reverter'
                )

                if old_destino:
                    self._aplicar_valor_saldo(
                        old_destino,
                        old_valor,
                        'Entrada',
                        operacao='reverter'
                    )

                # Aplicar novo valor
                self._aplicar_valor_saldo(
                    self.transacao_metodo,
                    self.transacao_valor,
                    self.transacao_entrada_saida,
                    operacao='adicionar'
                )

                if self.transacao_destino:
                    self._aplicar_valor_saldo(
                        self.transacao_destino,
                        self.transacao_valor,
                        'Entrada',
                        operacao='adicionar'
                    )

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Reverter o valor antes de deletar
            self._aplicar_valor_saldo(
                self.transacao_metodo,
                self.transacao_valor,
                self.transacao_entrada_saida,
                operacao='reverter'
            )

            if self.transacao_destino:
                self._aplicar_valor_saldo(
                    self.transacao_destino,
                    self.transacao_valor,
                    'Entrada',
                    operacao='reverter'
                )

            super().delete(*args, **kwargs)

    def _aplicar_valor_saldo(self, metodo, valor, entrada_saida, operacao):
        """
        Aplica ou reverte valor no saldo do método
        """
        if operacao == 'adicionar':
            if entrada_saida == 'Entrada':
                metodo.metodo_transacao_saldo += valor
            else:  # Saída
                metodo.metodo_transacao_saldo -= valor
        elif operacao == 'reverter':
            if entrada_saida == 'Entrada':
                metodo.metodo_transacao_saldo -= valor
            else:  # Saída
                metodo.metodo_transacao_saldo += valor

        metodo.save()

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
