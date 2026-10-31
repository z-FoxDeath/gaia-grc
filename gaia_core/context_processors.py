from django.db.models import Count
from apollo.models import Risco, Controle

def gaia_kpis(request):
    if request.path.startswith('/admin/'):
        riscos = Risco.objects.all()
        total_riscos = riscos.count()
        riscos_criticos = sum(1 for r in riscos if r.nivel_risco == "Crítico")
        total_controles = Controle.objects.count()

        # 1. Contagem Inerente (probabilidade x impacto)
        contagem_inerente = (
            Risco.objects.values('probabilidade', 'impacto')
            .annotate(total=Count('id'))
        )
        mapa_inerente = {
            (item['probabilidade'], item['impacto']): item['total']
            for item in contagem_inerente
        }

        # 2. Contagem Residual (probabilidade_residual x impacto_residual)
        contagem_residual = (
            Risco.objects.values('probabilidade_residual', 'impacto_residual')
            .annotate(total=Count('id'))
        )
        mapa_residual = {
            (item['probabilidade_residual'], item['impacto_residual']): item['total']
            for item in contagem_residual
        }

        # Função de coloração sólida e vibrante
        def obter_estilo_solido(p, i):
            score = p * i
            if score >= 15:
                # Crítico: Vermelho intenso com texto branco
                return "bg-red-600 hover:bg-red-700 text-white border-red-700 shadow-sm"
            elif score >= 10:
                # Alto: Laranja forte com texto branco
                return "bg-orange-500 hover:bg-orange-600 text-white border-orange-600 shadow-sm"
            elif score >= 5:
                # Moderado: Amarelo/Âmbar vivo com texto escuro
                return "bg-amber-400 hover:bg-amber-500 text-amber-950 border-amber-500 shadow-sm"
            # Baixo: Verde esmeralda com texto branco
            return "bg-emerald-600 hover:bg-emerald-700 text-white border-emerald-700 shadow-sm"

        # Construtor genérico de matriz 5x5
        def montar_grade(mapa_dados, parametro_prefixo=""):
            grade = []
            for impacto in range(5, 0, -1):
                linha = []
                for prob in range(1, 6):
                    qtd = mapa_dados.get((prob, impacto), 0)
                    linha.append({
                        'probabilidade': prob,
                        'impacto': impacto,
                        'total': qtd,
                        'classe_cor': obter_estilo_solido(prob, impacto),
                        'param_p': f"{parametro_prefixo}probabilidade__exact",
                        'param_i': f"{parametro_prefixo}impacto__exact",
                    })
                grade.append({
                    'nivel_impacto': impacto,
                    'colunas': linha
                })
            return grade

        matriz_inerente = montar_grade(mapa_inerente, "")
        matriz_residual = montar_grade(mapa_residual, "residual_")

        return {
            'total_riscos': total_riscos,
            'riscos_criticos': riscos_criticos,
            'total_controles': total_controles,
            'matriz_inerente': matriz_inerente,
            'matriz_residual': matriz_residual,
        }
    return {}