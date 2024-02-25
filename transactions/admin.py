from django.contrib import admin

from transactions.models import MetodoTransacao, Entrada


@admin.register(MetodoTransacao)
class MetodoTransacaoAdmin(admin.ModelAdmin):

    list_display = (
        'metodo_transacao_nome',
        'metodo_transacao_tipo'
    )

    exclude = ['metodo_transacao_usuario']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.filter(metodo_transacao_usuario=request.user)

    def save_model(self, request, obj, form, change):

        obj.metodo_transacao_usuario = request.user
        super().save_model(request, obj, form, change)
