from django.db import models
from eleuthia.models import Area
from apollo.models import Controle

class PlanoAnual(models.Model):
    ano = models.IntegerField(unique=True, verbose_name="Ano de Referência")
    descricao = models.TextField(blank=True, verbose_name="Descrição do Plano")
    aprovado = models.BooleanField(default=False, verbose_name="Plano Aprovado?")

    class Meta:
        verbose_name = 'Plano Anual de Auditoria'
        verbose_name_plural = 'Planos Anuais de Auditoria'
        ordering = ['-ano']

    def __str__(self):
        return f"Plano Anual - {self.ano}"

class Auditoria(models.Model):
    STATUS_CHOICES = [
        ('PLANEJADA', 'Planejada'),
        ('EXECUCAO', 'Em Execução'),
        ('RELATORIO', 'Relatório em Elaboração'),
        ('CONCLUIDA', 'Concluída'),
    ]
    
    plano = models.ForeignKey(PlanoAnual, on_delete=models.CASCADE, related_name='auditorias', verbose_name="Plano Anual")
    titulo = models.CharField(max_length=200, verbose_name="Título do Projeto")
    area_auditada = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Área Auditada")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANEJADA')
    data_inicio = models.DateField(null=True, blank=True, verbose_name="Data de Início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de Conclusão")

    class Meta:
        verbose_name = 'Projeto de Auditoria'
        verbose_name_plural = 'Projetos de Auditoria'
        ordering = ['data_inicio']

    def __str__(self):
        return self.titulo

class Apontamento(models.Model):
    GRAVIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    
    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name='apontamentos')
    controle_testado = models.ForeignKey(Controle, on_delete=models.PROTECT, verbose_name="Controle Avaliado", null=True, blank=True)
    titulo = models.CharField(max_length=200, verbose_name="Título do Achado")
    descricao = models.TextField(verbose_name="Descrição (Condição, Critério, Causa e Efeito)")
    gravidade = models.CharField(max_length=20, choices=GRAVIDADE_CHOICES, default='MEDIA')
    
    # NOVO CAMPO ADICIONADO:
    evidencia = models.FileField(upload_to='evidencias/%Y/%m/', null=True, blank=True, verbose_name="Evidência (Anexo)")

    class Meta:
        verbose_name = 'Apontamento / Achado'
        verbose_name_plural = 'Apontamentos / Achados'

    def __str__(self):
        return f"{self.auditoria.titulo} - {self.titulo}"