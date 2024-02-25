from django.contrib import admin

from transactions.models import MetodoTransacao, AreaTransacao, Entrada


@admin.register(MetodoTransacao)
class MetodoTransacaoAdmin(admin.ModelAdmin):

    exclude = ['user_connected']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.filter(user_connected=request.user)

    def save_model(self, request, obj, form, change):

        obj.user_connected = request.user
        super().save_model(request, obj, form, change)


@admin.register(AreaTransacao)
class AreaTransacaoAdmin(admin.ModelAdmin):

    exclude = ['user_connected']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.filter(user_connected=request.user)

    def save_model(self, request, obj, form, change):

        obj.user_connected = request.user
        super().save_model(request, obj, form, change)



@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):

    exclude = ['user_connected']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        print(qs)
        return qs.filter(user_connected=request.user)

    def save_model(self, request, obj, form, change):

        obj.user_connected = request.user
        super().save_model(request, obj, form, change)

    def render_change_form(self, request, context, *args, **kwargs):

        context['adminform'].form.fields['entrada_metodo_transacao'].queryset = MetodoTransacao.objects.filter(user_connected=request.user)
        context['adminform'].form.fields['entrada_area'].queryset = AreaTransacao.objects.filter(user_connected=request.user)

        return super().render_change_form(request, context, args, kwargs)
