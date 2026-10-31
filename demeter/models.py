from django.db import models
from django.contrib.auth.models import User
from aether.models import Apontamento

class PlanoAcao(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    apontamento = models.ForeignKey(Apontamento, on_delete=models.CASCADE, related_name='planos_acao', verbose_name="Apontamento/Achado")
    titulo = models.CharField(max_length=200, verbose_name="Título da Ação")
    descricao = models.TextField(verbose_name="Plano de Mitigação (O que será feito?)")
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Responsável pela Ação")
    prazo = models.DateField(verbose_name="Prazo de Conclusão")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')

    class Meta:
        verbose_name = 'Plano de Ação'
        verbose_name_plural = 'Planos de Ação'
        ordering = ['prazo']

    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"