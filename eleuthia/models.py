from django.db import models

class Filial(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome da Filial")
    sigla = models.CharField(max_length=10, unique=True)
    
    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Departamento(models.Model):
    filial = models.ForeignKey(Filial, on_delete=models.PROTECT, related_name='departamentos')
    nome = models.CharField(max_length=150)
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.filial.sigla}"


class Area(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='areas')
    nome = models.CharField(max_length=150, verbose_name="Nome da Área")
    
    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['nome']

    def __str__(self):
        return self.nome