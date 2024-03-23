from django.contrib import admin

from transactions.models import (
    MetodoTransacao,
    AreaTransacao,
    TipoTransacao,
    Entrada,
    Saida,

)


@admin.register(MetodoTransacao, AreaTransacao, TipoTransacao)
class FilterUserAdmin(admin.ModelAdmin):

    exclude = ['user_connected']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.filter(user_connected=request.user)

    def save_model(self, request, obj, form, change):

        obj.user_connected = request.user
        super().save_model(request, obj, form, change)


@admin.register(Entrada)
class EntradaAdmin(FilterUserAdmin):

    list_display = [
        'entrada_data',
        'entrada_area',
        'entrada_ds',
        'entrada_tipo',
        'entrada_valor',
        'entrada_metodo_transacao',
    ]

    list_filter = ['entrada_data', 'entrada_tipo']

    def render_change_form(self, request, context, *args, **kwargs):

        context['adminform'].form.fields['entrada_area'].queryset = AreaTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['entrada_tipo'].queryset = TipoTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['entrada_metodo_transacao'].queryset = MetodoTransacao.objects.filter(user_connected=request.user)

        return super().render_change_form(request, context, args, kwargs)


@admin.register(Saida)
class SaidaAdmin(FilterUserAdmin):

    list_display = [
        'saida_data',
        'saida_area',
        'colored_saida_ds',
        'colored_saida_tipo',
        'saida_valor',
        'saida_metodo_transacao',
    ]

    search_fields = ["saida_ds"]

    list_filter = ['saida_data', 'saida_tipo']

    def render_change_form(self, request, context, *args, **kwargs):

        context['adminform'].form.fields['saida_area'].queryset = AreaTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['saida_tipo'].queryset = TipoTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['saida_metodo_transacao'].queryset = MetodoTransacao.objects.filter(user_connected=request.user)

        return super().render_change_form(request, context, args, kwargs)
