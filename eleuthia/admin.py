from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Filial, Departamento, Area

@admin.register(Filial)
class FilialAdmin(ModelAdmin):
    list_display = ('nome', 'sigla')
    search_fields = ('nome', 'sigla')

@admin.register(Departamento)
class DepartamentoAdmin(ModelAdmin):
    list_display = ('nome', 'filial')
    list_filter = ('filial',)
    search_fields = ('nome',)

@admin.register(Area)
class AreaAdmin(ModelAdmin):
    list_display = ('nome', 'departamento')
    list_filter = ('departamento__filial', 'departamento')
    search_fields = ('nome',)