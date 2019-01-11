from django.contrib import admin

from .models import Produto, Pedido, ProdutoPedido, Carrinho


class ProdutoPedidoInline(admin.TabularInline):
    model = ProdutoPedido
    extra = 0


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria')

class PedidoAdmin(admin.ModelAdmin):
    fields = ('status_pedido',)
    list_display = ('id', 'owner', 'data', 'status_pedido', )
    inlines = [ProdutoPedidoInline]

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Carrinho)