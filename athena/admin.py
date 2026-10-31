from django.contrib import admin
from django.utils.html import format_html
from datetime import date
from unfold.admin import ModelAdmin
from .models import Politica

@admin.register(Politica)
class PoliticaAdmin(ModelAdmin):
    # Substituímos 'data_validade' pela nossa função customizada 'status_validade'
    list_display = ('codigo', 'titulo', 'tipo', 'versao', 'status', 'status_validade', 'dono')
    list_filter = ('status', 'tipo', 'area_gestora')
    search_fields = ('codigo', 'titulo')
    autocomplete_fields = ('dono',)

    def status_validade(self, obj):
        if not obj.data_validade:
            return format_html('<span style="color: gray;">Sem validade</span>')
        
        hoje = date.today()
        dias_restantes = (obj.data_validade - hoje).days

        if dias_restantes < 0:
            return format_html('<span style="color: #dc2626; font-weight: bold;">Vencida ({} dias)</span>', abs(dias_restantes))
        elif dias_restantes <= 30:
            return format_html('<span style="color: #ea580c; font-weight: bold;">Vence em {} dias</span>', dias_restantes)
        
        return format_html('<span style="color: #16a34a;">No prazo ({} dias)</span>', dias_restantes)
    
    status_validade.short_description = "Status de Validade"