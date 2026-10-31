from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ObrigacaoLegal, CampanhaCSA, AvaliacaoCSA

@admin.register(ObrigacaoLegal)
class ObrigacaoLegalAdmin(ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo', 'orgao_emissor')
    list_filter = ('tipo',)
    search_fields = ('codigo', 'nome', 'descricao')
    filter_horizontal = ('controles_associados',)

@admin.register(CampanhaCSA)
class CampanhaCSAAdmin(ModelAdmin):
    list_display = ('titulo', 'data_inicio', 'data_fim', 'status')
    list_filter = ('status',)
    search_fields = ('titulo',)

@admin.register(AvaliacaoCSA)
class AvaliacaoCSAAdmin(ModelAdmin):
    list_display = ('campanha', 'area_avaliada', 'controle', 'respondente', 'resposta')
    list_filter = ('resposta', 'campanha', 'area_avaliada')
    search_fields = ('controle__codigo', 'controle__nome')
    autocomplete_fields = ('respondente',)