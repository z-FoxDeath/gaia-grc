from django.db import models
from athena.models import Politica

from django.db import models

class Risco(models.Model):
    CATEGORIA_CHOICES = [
        ('ESTRATEGICO', 'Estratégico'),
        ('OPERACIONAL', 'Operacional'),
        ('FINANCEIRO', 'Financeiro'),
        ('COMPLIANCE', 'Compliance'),
    ]
    
    RESPOSTA_CHOICES = [
        ('ACEITAR', 'Aceitar'),
        ('EVITAR', 'Evitar'),
        ('REDUZIR', 'Reduzir'),
        ('COMPARTILHAR', 'Compartilhar'),
    ]
    
    PROBABILIDADE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    IMPACTO_CHOICES = [(i, str(i)) for i in range(1, 6)]

    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=200, verbose_name="Nome do Risco")
    descricao = models.TextField(verbose_name="Descrição Detalhada", blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='OPERACIONAL')
    
    # Risco Inerente (Sem controles)
    probabilidade = models.IntegerField(choices=PROBABILIDADE_CHOICES, default=3, verbose_name="Probabilidade Inerente")
    impacto = models.IntegerField(choices=IMPACTO_CHOICES, default=3, verbose_name="Impacto Inerente")
    
    # Risco Residual (Com os controles em atuação)
    probabilidade_residual = models.IntegerField(choices=PROBABILIDADE_CHOICES, default=2, verbose_name="Probabilidade Residual")
    impacto_residual = models.IntegerField(choices=IMPACTO_CHOICES, default=2, verbose_name="Impacto Residual")
    
    resposta = models.CharField(max_length=20, choices=RESPOSTA_CHOICES, default='REDUZIR', verbose_name="Resposta ao Risco")

    class Meta:
        verbose_name = 'Risco (COSO)'
        verbose_name_plural = 'Riscos (COSO)'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    @property
    def score_risco(self):
        """Calcula o score do Risco Inerente"""
        return self.probabilidade * self.impacto

    @property
    def nivel_risco(self):
        """Define a criticidade do Risco Inerente"""
        score = self.score_risco
        if score >= 15:
            return "Crítico"
        elif score >= 10:
            return "Alto"
        elif score >= 5:
            return "Moderado"
        return "Baixo"

    @property
    def score_residual(self):
        """Calcula o score do Risco Residual"""
        return self.probabilidade_residual * self.impacto_residual

    @property
    def nivel_residual(self):
        """Define a criticidade do Risco Residual"""
        score = self.score_residual
        if score >= 15:
            return "Crítico"
        elif score >= 10:
            return "Alto"
        elif score >= 5:
            return "Moderado"
        return "Baixo"

class Framework(models.Model):
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código") # <-- Garanta que este campo existe aqui
    nome = models.CharField(max_length=150, verbose_name="Nome do Framework (Ex: ISO 27001, CIS v8)")
    descricao = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name = 'Framework'
        verbose_name_plural = 'Frameworks'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class RequisitoNormativo(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE, related_name='requisitos')
    codigo = models.CharField(max_length=50, verbose_name="Domínio/Cláusula")
    descricao = models.TextField(verbose_name="Descrição do Requisito")

    class Meta:
        verbose_name = 'Requisito Normativo'
        verbose_name_plural = 'Requisitos Normativos'
        ordering = ['framework', 'codigo']

    def __str__(self):
        return f"{self.framework.nome} - {self.codigo}"

class Controle(models.Model):
    TIPO_CHOICES = [
        ('PREVENTIVO', 'Preventivo'),
        ('DETECTIVO', 'Detectivo'),
        ('CORRETIVO', 'Corretivo'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=150, verbose_name="Nome do Controle")
    descricao = models.TextField(verbose_name="Descrição do Controle")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PREVENTIVO')
    
    # Relacionamentos que o admin está a procurar:
    riscos = models.ManyToManyField(
        Risco, 
        related_name='controles_mitigadores', 
        blank=True,
        verbose_name="Riscos Mitigados"
    )
    
    requisitos = models.ManyToManyField(
        'RequisitoNormativo', 
        related_name='controles', 
        blank=True,
        verbose_name="Requisitos Normativos Atendidos"
    )
    
    politicas = models.ManyToManyField(
        'athena.Politica', # Assumindo que a política vem do app athena (ou ajuste se estiver no mesmo app)
        related_name='controles', 
        blank=True,
        verbose_name="Políticas Relacionadas"
    )

    class Meta:
        verbose_name = 'Controle Interno'
        verbose_name_plural = 'Controles Internos'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"