from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from eleuthia.models import Departamento, Area, Filial
from hephaestus.models import Processo, Subprocesso
from athena.models import Politica
from apollo.models import Risco, Controle, Framework

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula a base com estrutura organizacional completa e riscos do GAIA.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("A iniciar a criação da base integrada do GAIA..."))

        # 1. Estrutura Organizacional (Eleuthia)
        filial_matriz, _ = Filial.objects.get_or_create(
            sigla="FIL-01",
            defaults={"nome": "Matriz Corporativa"}
        )

        dep_ti, _ = Departamento.objects.get_or_create(
            nome="Tecnologia da Informação e Segurança",
            filial=filial_matriz
        )
        dep_fin, _ = Departamento.objects.get_or_create(
            nome="Controladoria e Finanças",
            filial=filial_matriz
        )

        area_sec, _ = Area.objects.get_or_create(
            nome="Segurança Cibernética e Governança de TI",
            departamento=dep_ti
        )

        # 2. Pessoas / Usuários de Teste
        User.objects.get_or_create(
            username="carlos.gestor",
            defaults={"first_name": "Carlos", "last_name": "Eduardo", "email": "carlos.ti@empresa.com"}
        )
        User.objects.get_or_create(
            username="mariana.fin",
            defaults={"first_name": "Mariana", "last_name": "Souza", "email": "mariana.fin@empresa.com"}
        )

        # 3. Gestão de Processos (Hephaestus - informando o 'codigo' obrigatório)
        proc_iam, _ = Processo.objects.get_or_create(
            codigo="PRC-TI-01",
            defaults={
                "nome": "Gestão de Identidades, Acessos e Credenciais",
                "area": area_sec
            }
        )
        Subprocesso.objects.get_or_create(
            nome="Revisão Periódica de Contas",
            defaults={"processo": proc_iam}
        )

        Processo.objects.get_or_create(
            codigo="PRC-FIN-01",
            defaults={
                "nome": "Processamento de Pagamentos e Conciliação Bancária",
                "area": area_sec
            }
        )

        # 4. Políticas Corporativas (Athena)
        Politica.objects.get_or_create(
            codigo="POL-SEC-01",
            defaults={
                "titulo": "Política de Segurança da Informação (PSI)",
                "versao": "2.1",
                "status": "APROVADA"
            }
        )

        # 5. Frameworks Normativos (Apollo)
        Framework.objects.get_or_create(
            codigo="COSO-ERM",
            defaults={"nome": "COSO Enterprise Risk Management", "descricao": "Governança e Gestão de Riscos"}
        )
        Framework.objects.get_or_create(
            codigo="ISO-27001",
            defaults={"nome": "ISO/IEC 27001:2022", "descricao": "Segurança da Informação"}
        )

        # 6. Controles Internos (Apollo)
        ctrl_iam, _ = Controle.objects.get_or_create(
            codigo="CTRL-IAM-01",
            defaults={
                "nome": "Revisão Periódica de Acessos a Aplicações Críticas",
                "descricao": "Auditoria de permissões e contas inativas em sistemas corporativos.",
                "tipo": "DETECTIVO"
            }
        )
        ctrl_mfa, _ = Controle.objects.get_or_create(
            codigo="CTRL-SEC-02",
            defaults={
                "nome": "Autenticação Multifator Obrigatória",
                "descricao": "Segundo fator de autenticação para acessos externos e servidores.",
                "tipo": "PREVENTIVO"
            }
        )
        ctrl_sod, _ = Controle.objects.get_or_create(
            codigo="CTRL-FIN-01",
            defaults={
                "nome": "Segregação de Funções no ERP Financeiro",
                "descricao": "Bloqueio de autorização mútua entre cadastro de contas e desembolso.",
                "tipo": "PREVENTIVO"
            }
        )

        # 7. Riscos Corporativos (Matriz 5x5: Inerente vs. Residual)
        dados_riscos = [
            (
                "RSK-TI-01",
                "Acesso indevido a dados sensíveis por privilégios excessivos",
                "COMPLIANCE", 5, 5, 2, 2, "REDUZIR", [ctrl_iam, ctrl_mfa]
            ),
            (
                "RSK-TI-02",
                "Indisponibilidade operacional crítica decorrente de Ransomware",
                "OPERACIONAL", 4, 5, 2, 3, "REDUZIR", [ctrl_mfa]
            ),
            (
                "RSK-FIN-01",
                "Fraude financeira decorrente da ausência de alçada dupla",
                "FINANCEIRO", 4, 4, 1, 2, "REDUZIR", [ctrl_sod]
            ),
            (
                "RSK-EST-01",
                "Atraso na adaptação a novas diretrizes regulatórias e fiscais",
                "ESTRATEGICO", 4, 3, 3, 3, "ACEITAR", []
            ),
            (
                "RSK-OP-01",
                "Interrupção de atividades críticas por rotatividade de pessoal chave",
                "OPERACIONAL", 5, 2, 3, 2, "REDUZIR", []
            ),
            (
                "RSK-TI-03",
                "Vazamento acidental de credenciais administrativas em repositórios",
                "COMPLIANCE", 3, 5, 1, 4, "REDUZIR", [ctrl_iam]
            ),
            (
                "RSK-FIN-02",
                "Impacto no fluxo de caixa por inadimplência acima do projetado",
                "FINANCEIRO", 3, 3, 2, 2, "COMPARTILHAR", []
            ),
            (
                "RSK-OP-02",
                "Inconsistência manual em relatórios contábeis de fechamento",
                "OPERACIONAL", 3, 2, 2, 1, "REDUZIR", [ctrl_sod]
            ),
            (
                "RSK-TI-04",
                "Oscilação pontual de link redundante sem impacto na operação",
                "OPERACIONAL", 2, 2, 1, 1, "ACEITAR", []
            ),
            (
                "RSK-EST-02",
                "Desalinhamento estratégico entre metas de negócios e capacidade de TI",
                "ESTRATEGICO", 2, 4, 2, 3, "EVITAR", []
            ),
        ]

        for cod, nome, cat, pi, ii, pr, ir, resp, ctrls in dados_riscos:
            risco, created = Risco.objects.get_or_create(
                codigo=cod,
                defaults={
                    "nome": nome,
                    "categoria": cat,
                    "probabilidade": pi,
                    "impacto": ii,
                    "probabilidade_residual": pr,
                    "impacto_residual": ir,
                    "resposta": resp,
                    "descricao": f"Risco operacional monitorado pelo GAIA ({cod})."
                }
            )
            if created and ctrls:
                for c in ctrls:
                    c.riscos.add(risco)

        self.stdout.write(self.style.SUCCESS("Base integrada populada com sucesso!"))