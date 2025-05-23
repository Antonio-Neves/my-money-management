from django.contrib import admin


from transactions.models import (
    AreaTransacao,
    TipoTransacao,
    MetodoTransacao,
    Transacao,
)


@admin.register(AreaTransacao, TipoTransacao, MetodoTransacao)
class FilterUserAdmin(admin.ModelAdmin):

    exclude = ['user_connected']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.filter(user_connected=request.user)

    def save_model(self, request, obj, form, change):

        obj.user_connected = request.user
        super().save_model(request, obj, form, change)


@admin.register(Transacao)
class TransacaoAdmin(FilterUserAdmin):

    def get_changeform_initial_data(self, request):
        """
        Define valores iniciais para o formulário no admin.
        """
        initial = super().get_changeform_initial_data(request)
        initial['transacao_entrada_saida'] = 'S'  # Defina o valor inicial aqui
        return initial

    list_display = [
        'transacao_data',
        'transacao_area',
        'colored_transacao_descricao',
        'transacao_valor',
        'transacao_metodo',
        'colored_transacao_tipo',
        'transacao_destino',
        'transacao_entrada_saida'
    ]

    search_fields = ["transacao_descricao"]

    list_filter = ['transacao_data', 'transacao_entrada_saida', 'transacao_tipo']

    def render_change_form(self, request, context, *args, **kwargs):

        context['adminform'].form.fields['transacao_area'].queryset = AreaTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['transacao_tipo'].queryset = TipoTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['transacao_metodo'].queryset = MetodoTransacao.objects.filter(user_connected=request.user)

        return super().render_change_form(request, context, args, kwargs)
