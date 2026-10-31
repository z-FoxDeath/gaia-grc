from django.db import models
from django.contrib.auth.models import User
from eleuthia.models import Area

class Politica(models.Model):
    TIPO_CHOICES = [
        ('POLITICA', 'Política'),
        ('NORMA', 'Norma'),
        ('PROCEDIMENTO', 'Procedimento (POP)'),
        ('MANUAL', 'Manual'),
    ]
    
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('VIGENTE', 'Vigente'),
        ('REVISAO', 'Em Revisão'),
        ('OBSOLETA', 'Obsoleta'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    titulo = models.CharField(max_length=200, verbose_name="Título do Documento")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='POLITICA')
    area_gestora = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Área Gestora")
    dono = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Dono (Owner)")
    
    versao = models.CharField(max_length=10, default="1.0", verbose_name="Versão")
    data_publicacao = models.DateField(null=True, blank=True, verbose_name="Data de Publicação")
    data_validade = models.DateField(null=True, blank=True, verbose_name="Válida até")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    
    # Requer que a configuração MEDIA_URL esteja ativa (o que já fizemos no passo de Evidências)
    documento = models.FileField(upload_to='politicas/%Y/%m/', null=True, blank=True, verbose_name="Arquivo (PDF/DOCX)")

    class Meta:
        verbose_name = 'Política Interna'
        verbose_name_plural = 'Políticas Internas'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.titulo} (v{self.versao})"