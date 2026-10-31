from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from datetime import date, timedelta
from athena.models import Politica

class Command(BaseCommand):
    help = 'Verifica políticas vencendo em 30 dias e envia alerta de e-mail ao dono.'

    def handle(self, *args, **kwargs):
        hoje = date.today()
        limite_alerta = hoje + timedelta(days=30)

        # Busca políticas vigentes que vencem nos próximos 30 dias ou já venceram
        politicas_alerta = Politica.objects.filter(
            status='VIGENTE',
            data_validade__lte=limite_alerta
        )

        if not politicas_alerta:
            self.stdout.write(self.style.SUCCESS("Nenhuma política próxima do vencimento."))
            return

        for politica in politicas_alerta:
            dias = (politica.data_validade - hoje).days
            status_txt = f"vence em {dias} dias" if dias >= 0 else f"ESTÁ VENCIDA há {abs(dias)} dias"
            
            assunto = f"[GAIA GRC] Alerta de Validade: {politica.codigo}"
            mensagem = f"Olá,\n\nA política '{politica.titulo}' (Versão {politica.versao}) {status_txt}.\nPor favor, inicie o processo de revisão."
            
            # Como configuramos EMAIL_BACKEND para 'console', isso será impresso no terminal
            send_mail(
                assunto,
                mensagem,
                'nao-responda@gaiagrc.com',
                [politica.dono.email] if politica.dono.email else ['admin@gaiagrc.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.WARNING(f"Alerta gerado para: {politica.codigo}"))

        self.stdout.write(self.style.SUCCESS(f"Rotina concluída. {politicas_alerta.count()} alertas gerados."))