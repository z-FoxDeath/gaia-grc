from django.contrib import admin
from django.http import HttpResponse
from unfold.admin import ModelAdmin
from unfold.decorators import action
from reportlab.pdfgen import canvas
from .models import PlanoAcao

@admin.register(PlanoAcao)
class PlanoAcaoAdmin(ModelAdmin):
    list_display = ('titulo', 'apontamento', 'responsavel', 'prazo', 'status')
    list_filter = ('status', 'prazo')
    search_fields = ('titulo', 'descricao')
    
    # Registra a nossa função customizada no menu de ações do Unfold
    actions = ['exportar_relatorio_pdf']

    @action(description="Exportar selecionados para PDF")
    def exportar_relatorio_pdf(self, request, queryset):
        # Prepara a resposta do navegador para baixar um arquivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_planos_acao.pdf"'
        
        # Inicia o "desenho" do PDF
        p = canvas.Canvas(response)
        y = 800  # Posição inicial no eixo Y (de cima para baixo)
        
        # Cabeçalho do PDF
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y, "Relatório de Planos de Ação - GAIA GRC")
        y -= 40
        
        # Corpo do PDF iterando sobre os itens que você selecionou na tela
        p.setFont("Helvetica", 11)
        for plano in queryset:
            # Se a página encher, cria uma nova
            if y < 100:
                p.showPage()
                p.setFont("Helvetica", 11)
                y = 800
                
            linha = f"Ação: {plano.titulo} | Prazo: {plano.prazo} | Status: {plano.get_status_display()}"
            p.drawString(100, y, linha)
            y -= 25
            
        p.showPage()
        p.save()
        
        return response