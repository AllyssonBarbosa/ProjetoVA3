from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Produto, Venda
from .forms import ProdutoForm
from datetime import datetime
from decimal import Decimal
from django.utils import timezone

def index(request):
    user = request.user
    is_limited_user = user.groups.filter(name='Limitados').exists()
    return render(request, 'index.html', {'is_limited_user': is_limited_user})

def produto(request, pk):
    prod = get_list_or_404(Produto, id=pk)
    context = {'produto': prod}
    return render(request, 'produto.html', context)

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produto')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})

def listar_produto(request):
    produtos = Produto.objects.all()
    mensagem = "Nenhum produto cadastrado." if not produtos else None
    return render(request, 'listar_produto.html', {'produtos': produtos, 'mensagem': mensagem})

def buscar_produto(request):
    query_nome = request.GET.get('q_nome')
    query_id = request.GET.get('q_id')
    produtos_por_nome = []
    produto_por_id = None
    usuario_limitado = request.user.groups.filter(name='Limitados').exists()

    if query_id:
        try:
            produto_por_id = Produto.objects.get(id=query_id)
        except (Produto.DoesNotExist, ValueError):
            pass
    elif query_nome:
        produtos_por_nome = Produto.objects.filter(nome__icontains=query_nome)

    context = {
        'query_nome': query_nome,
        'query_id': query_id,
        'produto_por_id': produto_por_id,
        'produtos_por_nome': produtos_por_nome,
        'usuario_limitado': usuario_limitado
    }
    return render(request, 'buscar_produto.html', context)

def modificar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome')
        novo_valor = request.POST.get('novo_valor')
        novo_quantidade = request.POST.get('novo_quantidade')
        nova_imagem = request.FILES.get('nova_imagem')

        if novo_nome:
            produto.nome = novo_nome
        if novo_valor:
            produto.valor = novo_valor
        if novo_quantidade:
            produto.quantidade = novo_quantidade
        if nova_imagem:
            produto.foto.delete()
            produto.foto = nova_imagem

        produto.save()
        return redirect('buscar_produto')

    context = {'produto': produto}
    return render(request, 'modificar_produto.html', context)

from decimal import Decimal
from datetime import datetime

def realizar_venda(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade_str = request.POST.get('quantidade')
        data_str = request.POST.get('data')


        if quantidade_str:
            quantidade = int(quantidade_str)
        else:
            quantidade = 0


        produto = Produto.objects.get(id=produto_id)


        if quantidade > produto.quantidade:
            return render(request, 'realizar_venda.html', {
                'produto': produto,
                'hoje': datetime.now(),
                'error_message': 'Quantidade insuficiente em estoque'
            })


        valor_total = Decimal(produto.valor) * quantidade
        data_venda = datetime.now().date()


        venda = Venda.objects.create(
            produto=produto,
            quantidade=quantidade,
            valor_total=valor_total,
            data_venda=data_venda,
            user=request.user
        )


        produto.quantidade -= quantidade
        produto.save()

        return render(request, 'realizar_venda.html', {
            'produto': produto,
            'hoje': datetime.now()
        })


    produtos = Produto.objects.all()
    hoje = datetime.now()
    return render(request, 'realizar_venda.html', {
        'produtos': produtos,
        'hoje': hoje
    })

def deletar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    return redirect('listar_produto')
def calcular_valor_total_estoque():
    return Produto.objects.annotate(valor_total_estoque=F('quantidade') * F('valor')).aggregate(total_estoque=Sum('valor_total_estoque'))['total_estoque']

from django.shortcuts import render, get_object_or_404



from django.shortcuts import render
from django.db.models import Sum, F
from django.utils import timezone
from core.models import Venda, Produto

def estatisticas_vendas(request):
    mes_atual = timezone.now().month
    ano_atual = timezone.now().year

    vendas = Venda.objects.all().select_related('produto').order_by('-data_venda')
    produtos_vendidos = Venda.objects.filter(data_venda__month=mes_atual).select_related('produto').order_by('-data_venda')

    quantidade_total_estoque = Produto.objects.aggregate(total_estoque=Sum('quantidade'))['total_estoque']
    valor_vendas_mes = produtos_vendidos.aggregate(valor_mes=Sum('valor_total'))['valor_mes']
    valor_vendas_ano = Venda.objects.filter(data_venda__year=ano_atual).aggregate(valor_ano=Sum('valor_total'))['valor_ano']

    produto_mais_vendido = produtos_vendidos.values('produto__nome').annotate(quantidade_vendida=Sum('quantidade')).order_by('-quantidade_vendida').first()
    produto_menos_vendido = produtos_vendidos.values('produto__nome').annotate(quantidade_vendida=Sum('quantidade')).order_by('quantidade_vendida').first()

    valor_total_estoque = calcular_valor_total_estoque()

    context = {
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
        'vendas': vendas,
        'produtos_vendidos': produtos_vendidos,
        'quantidade_total_estoque': quantidade_total_estoque,
        'valor_vendas_mes': valor_vendas_mes,
        'valor_vendas_ano': valor_vendas_ano,
        'produto_mais_vendido': produto_mais_vendido,
        'produto_menos_vendido': produto_menos_vendido,
        'valor_total_estoque': valor_total_estoque,
    }

    return render(request, 'estatisticas_vendas.html', context)

def calcular_valor_total_estoque():
    return Produto.objects.annotate(valor_total_estoque=F('quantidade') * F('valor')).aggregate(total_estoque=Sum('valor_total_estoque'))['total_estoque']




def excluir_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)

    produto = venda.produto
    produto.quantidade += venda.quantidade
    produto.save()

    venda.delete()

    return redirect('estatisticas_vendas')

from django.db.models import Sum

def estatisticas_anuais(request):
    ano_selecionado = request.GET.get('ano')
    ano = None
    vendas_ano = []
    total_vendas_ano = 0

    if ano_selecionado:
        try:
            ano = int(ano_selecionado)
            vendas_ano = Venda.objects.filter(data_venda__year=ano).order_by('-data_venda')
            total_vendas_ano = vendas_ano.aggregate(total=Sum('valor_total'))['total'] or 0
        except ValueError:
            pass

    return render(request, 'estatisticas_anuais.html', {
        'ano': ano,
        'vendas_ano': vendas_ano,
        'total_vendas_ano': total_vendas_ano,
    })

def grafico_vendas_mes_a_mes(request, ano):
    vendas_por_mes = Venda.objects.filter(data_venda__year=ano).values('data_venda__month').annotate(total=Sum('valor_total'))

    meses = [str(mes['data_venda__month']) for mes in vendas_por_mes]
    valores = [mes['total'] for mes in vendas_por_mes]

    context = {
        'ano': ano,
        'meses': meses,
        'valores': valores,
    }

    return render(request, 'grafico_vendas_mes_a_mes.html', context)

def produtos_estoque(request):
    produtos_0 = Produto.objects.filter(quantidade__in=[0]).order_by('nome')
    produtos_1 = Produto.objects.filter(quantidade__in=[1]).order_by('nome')
    produtos_2 = Produto.objects.filter(quantidade__in=[2]).order_by('nome')
    produtos_3 = Produto.objects.filter(quantidade__in=[3]).order_by('nome')

    context = {
        'produtos_0': produtos_0,
        'produtos_1': produtos_1,
        'produtos_2': produtos_2,
        'produtos_3': produtos_3,
    }
    return render(request, 'produtos_estoque.html', context)

import logging

logger = logging.getLogger(__name__)

def estatisticas_mensais(request):
    ano_selecionado = request.GET.get('ano')
    meses = [
        ('01', 'Janeiro'), ('02', 'Fevereiro'), ('03', 'Março'),
        ('04', 'Abril'), ('05', 'Maio'), ('06', 'Junho'),
        ('07', 'Julho'), ('08', 'Agosto'), ('09', 'Setembro'),
        ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')
    ]
    vendas_mensais = {}
    total_vendas_ano = 0
    ano = None

    if ano_selecionado:
        try:
            ano = int(ano_selecionado)
            logger.info(f"Ano selecionado: {ano}")

            for mes, nome_mes in meses:
                logger.info(f"Consultando mês: {mes}")
                vendas = Venda.objects.filter(data_venda__year=ano, data_venda__month=int(mes))
                total_vendas_mes = vendas.aggregate(total=Sum('valor_total'))['total'] or 0
                vendas_mensais[mes] = {
                    'nome_mes': nome_mes,
                    'total_vendas_mes': total_vendas_mes
                }
                total_vendas_ano += total_vendas_mes

        except ValueError as e:
            logger.error(f"Erro ao converter ano: {e}")

    return render(request, 'estatisticas_mensais.html', {
        'ano': ano,
        'vendas_mensais': vendas_mensais,
        'total_vendas_ano': total_vendas_ano,
    })

def cancelar_venda(request, venda_id):
    if not request.user.has_perm('app_name.cancelar_venda'):
        return HttpResponseForbidden("Você não tem permissão para cancelar esta venda.")

    venda = get_object_or_404(Venda, id=venda_id)
    venda.delete()

    return redirect('estatisticas_vendas')
