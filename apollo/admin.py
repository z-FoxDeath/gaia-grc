from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Risco, Controle, Framework, RequisitoNormativo

@admin.register(Risco)
class RiscoAdmin(ModelAdmin):
    list_display = (
        'codigo', 
        'nome', 
        'categoria', 
        'status_nivel_risco',          # Inerente
        'status_nivel_residual',       # Residual
        'resposta'
    )
    list_filter = ('categoria', 'resposta', 'probabilidade', 'probabilidade_residual')
    search_fields = ('codigo', 'nome')

    def _format_badge(self, nivel, score):
        cores = {
            'Crítico': '#dc2626',   # Vermelho forte
            'Alto': '#ea580c',      # Laranja
            'Moderado': '#ca8a04',  # Amarelo/Dourado
            'Baixo': '#16a34a',     # Verde
        }
        cor = cores.get(nivel, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{} ({})</span>',
            cor, nivel, score
        )

    def status_nivel_risco(self, obj):
        return self._format_badge(obj.nivel_risco, obj.score_risco)
    status_nivel_risco.short_description = "Risco Inerente"

    def status_nivel_residual(self, obj):
        return self._format_badge(obj.nivel_residual, obj.score_residual)
    status_nivel_residual.short_description = "Risco Residual"

@admin.register(Controle)
class ControleAdmin(ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('codigo', 'nome')
    filter_horizontal = ('riscos', 'requisitos', 'politicas') # Permite associar os r

@admin.register(Framework)
class FrameworkAdmin(ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')

@admin.register(RequisitoNormativo)
class RequisitoNormativoAdmin(ModelAdmin):
    list_display = ('codigo', 'framework', 'descricao_resumida')
    list_filter = ('framework',)
    search_fields = ('codigo', 'descricao')

    def descricao_resumida(self, obj):
        return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
    descricao_resumida.short_description = "Descrição"