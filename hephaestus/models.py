from django.db import models
from eleuthia.models import Area
from apollo.models import Risco

class Processo(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='processos', verbose_name="Área Responsável")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=200, verbose_name="Nome do Processo")
    descricao = models.TextField(verbose_name="Descrição do Processo", blank=True)
    
    # É aqui que amarramos Hephaestus a Apollo!
    riscos_associados = models.ManyToManyField(Risco, related_name='processos', blank=True, verbose_name="Riscos Mapeados")

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.area.nome})"

class Subprocesso(models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='subprocessos', verbose_name="Processo Macro")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=200, verbose_name="Nome do Subprocesso")
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Subprocesso'
        verbose_name_plural = 'Subprocessos'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"