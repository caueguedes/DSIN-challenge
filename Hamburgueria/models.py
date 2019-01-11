from django.db import models
from django.core.validators import MinValueValidator


class Pedido(models.Model):
    STATUSES = (
        ('P', 'Pedido Efetuado'),
        ('A', 'Em Andamento'),
        ('E', 'Entregando'),
        ('X', 'Entregue'),
        ('C', 'Carrinho'),
    )
    status_pedido = models.CharField(max_length=1, choices=STATUSES, default='P')
    owner = models.ForeignKey('auth.User', related_name='pedidos', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    # status_pedido = models.BooleanField(default=False)

    def __str__(self):
        return 'Pedido nr' + str(self.id) + ' de ' + str(self.owner)

    class Meta:
        verbose_name = ("Pedido")
        verbose_name_plural = ("Pedidos")


class Produto(models.Model):
    FOOD_CATEGORY = (
        ('L', 'Lanches'),
        ('B', 'Bebidas'),
        ('S', 'Sobremesas'),
    )
    categoria = models.CharField(max_length=1, choices=FOOD_CATEGORY)
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=800, default='')


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = ("Produto")
        verbose_name_plural = ("Produtos")


class ProdutoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='Pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='Produto', on_delete=models.CASCADE)
    qtd = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return 'Pedido nr:' +  str(self.pedido.id) + ' produto ' + str(self.produto)

    class Meta:
        verbose_name = ("ProdutoPedidos")
        verbose_name_plural = ("ProdutosPedido")


class Carrinho(models.Model):
    owner = models.ForeignKey('auth.User', related_name='CarrinhoItem', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='Carrinho', on_delete=models.CASCADE)
    qtd = models.IntegerField(default=1)
