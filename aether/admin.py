from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PlanoAnual, Auditoria, Apontamento

@admin.register(PlanoAnual)
class PlanoAnualAdmin(ModelAdmin):
    list_display = ('ano', 'aprovado')
    list_filter = ('aprovado',)
    search_fields = ('ano',)

@admin.register(Auditoria)
class AuditoriaAdmin(ModelAdmin):
    list_display = ('titulo', 'plano', 'area_auditada', 'status', 'data_inicio')
    list_filter = ('status', 'plano', 'area_auditada')
    search_fields = ('titulo',)

@admin.register(Apontamento)
class ApontamentoAdmin(ModelAdmin):
    list_display = ('titulo', 'auditoria', 'controle_testado', 'gravidade')
    list_filter = ('gravidade', 'auditoria')
    search_fields = ('titulo', 'descricao')