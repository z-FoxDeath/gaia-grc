from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Processo, Subprocesso

@admin.register(Processo)
class ProcessoAdmin(ModelAdmin):
    list_display = ('codigo', 'nome', 'area')
    list_filter = ('area__departamento__filial', 'area') # Filtro em cascata: Filial > Depto > Área
    search_fields = ('codigo', 'nome')
    filter_horizontal = ('riscos_associados',) # Cria a caixinha elegante para selecionar os riscos

@admin.register(Subprocesso)
class SubprocessoAdmin(ModelAdmin):
    list_display = ('codigo', 'nome', 'processo')
    list_filter = ('processo__area', 'processo')
    search_fields = ('codigo', 'nome')