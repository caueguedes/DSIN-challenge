from Hamburgueria.models import Produto, Pedido, ProdutoPedido, Carrinho
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.db.models import Sum


def home(request):
    context= {}
    context['usr'] = request.user.is_authenticated
    context['staff'] = request.user.is_staff
    context['produtos'] = Produto.objects.all()
    if request.user.is_authenticated:
        context['carrinho'] = Carrinho.objects.filter(owner=request.user).aggregate(Sum('qtd'))['qtd__sum']
        context['listaCarrinho'] = Carrinho.objects.filter(owner=request.user)
    return render(request, 'Hamburgueria/homeCli.html', context)


def pedidos(request):
    context = {}
    context['carrinho'] = Carrinho.objects.filter(owner=request.user).aggregate(Sum('qtd'))['qtd__sum']
    context['listaCarrinho'] = Carrinho.objects.filter(owner=request.user)
    context['usr'] = request.user.is_authenticated
    context['staff'] = request.user.is_staff
    if request.user.is_authenticated:
        historico = Pedido.objects.filter(owner_id=request.user.id)
        produtos = ProdutoPedido.objects.filter(pedido__owner_id=request.user.id)
        context['historico'] = historico
        context['produtos'] = produtos
    return render(request, 'Hamburgueria/pedidos.html', context)


def detalhes(request):
    context = {}
    context['usr'] = request.user.is_authenticated
    context['staff'] = request.user.is_staff
    pk = request.data['pk']
    if request.user.is_authenticated:
        pedido = ProdutoPedido.objects.filter(pedido__id=pk)
        context['pedido'] = pedido
    return render(request, 'Hamburgueria/pedidos.html', context)


def addProduto(request, pk):
    produto = Carrinho.objects.filter(Q(owner=request.user), Q(produto=pk))
    prod = Produto.objects.get(pk=pk)
    if len(produto):
        produto = produto[0]
        produto.qtd += 1
        produto.save()
    else:
        Carrinho.objects.create(produto=prod, qtd=1, owner_id=request.user.id)
    return redirect('ham:home')


def fechaProduto(request):
    carrinho = Carrinho.objects.filter(owner=request.user.id)
    if carrinho:
        pedido = Pedido.objects.create(owner=request.user)
        for item in carrinho:
            prodPedido = ProdutoPedido.objects.create(pedido=pedido, produto_id=item.produto.id, qtd=item.qtd)
            item.delete()
    return redirect('ham:home')


def removeProduto(request, pk):
    produto = Carrinho.objects.filter(Q(owner=request.user), Q(produto=pk))
    produto.delete()
    return redirect('ham:home')


def cancelaPedido(request, pk):
    prodPedido = ProdutoPedido.objects.filter(pedido=pk)
    pedido = Pedido.objects.get(pk=pk)
    if prodPedido:
        for item in prodPedido:
            carrinho = Carrinho.objects.create(owner=request.user, produto=item.produto, qtd=item.qtd)
            item.delete()
    pedido.delete()
    return redirect('ham:pedidos')
