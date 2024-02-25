from django.contrib import admin

from transactions.models import MetodoTransacao, Entrada


@admin.register(MetodoTransacao)
class MetodoTransacaoAdmin(admin.ModelAdmin):

    list_display = (
        'metodo_transacao_nome',
        'metodo_transacao_tipo'
    )

    exclude = ['user_connected']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.filter(user_connected=request.user)

    def save_model(self, request, obj, form, change):

        obj.user_connected = request.user
        super().save_model(request, obj, form, change)
