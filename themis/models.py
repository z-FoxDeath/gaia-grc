from django.db import models
from django.contrib.auth.models import User
from apollo.models import Controle
from eleuthia.models import Area

class ObrigacaoLegal(models.Model):
    TIPO_CHOICES = [
        ('LEI', 'Lei / Decreto'),
        ('REGULAMENTACAO', 'Regulamentação (BACEN, CVM, etc)'),
        ('CONTRATO', 'Cláusula Contratual'),
    ]

    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código/Artigo")
    nome = models.CharField(max_length=200, verbose_name="Nome da Obrigação (Ex: LGPD, SOX)")
    descricao = models.TextField(verbose_name="Descrição da Exigência")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='LEI')
    orgao_emissor = models.CharField(max_length=100, verbose_name="Órgão Emissor / Regulador", blank=True)
    
    # Amarra a Lei aos nossos Controles
    controles_associados = models.ManyToManyField(Controle, related_name='obrigacoes_legais', blank=True)

    class Meta:
        verbose_name = 'Obrigação Legal'
        verbose_name_plural = 'Obrigações Legais'
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class CampanhaCSA(models.Model):
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('ABERTA', 'Em Andamento (Aberta)'),
        ('FECHADA', 'Concluída / Fechada'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Nome da Campanha (Ex: CSA 2026 - Q3)")
    data_inicio = models.DateField()
    data_fim = models.DateField(verbose_name="Prazo de Resposta")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')

    class Meta:
        verbose_name = 'Campanha CSA'
        verbose_name_plural = 'Campanhas CSA'
        ordering = ['-data_inicio']

    def __str__(self):
        return self.titulo

class AvaliacaoCSA(models.Model):
    RESPOSTA_CHOICES = [
        ('PENDENTE', 'Pendente de Resposta'),
        ('EFETIVO', 'Sim, operando efetivamente'),
        ('INEFETIVO', 'Não, apresenta falhas'),
        ('NAO_APLICA', 'Não se aplica ao meu processo'),
    ]

    campanha = models.ForeignKey(CampanhaCSA, on_delete=models.CASCADE, related_name='avaliacoes')
    area_avaliada = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Área Avaliada")
    controle = models.ForeignKey(Controle, on_delete=models.PROTECT, verbose_name="Controle Avaliado")
    respondente = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Gestor Responsável")
    
    resposta = models.CharField(max_length=20, choices=RESPOSTA_CHOICES, default='PENDENTE')
    justificativa = models.TextField(blank=True, verbose_name="Justificativa (Obrigatória se Inefetivo ou N/A)")
    data_resposta = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Resposta do CSA'
        verbose_name_plural = 'Respostas do CSA'

    def __str__(self):
        return f"{self.campanha} | {self.controle.codigo} | {self.area_avaliada.nome}"