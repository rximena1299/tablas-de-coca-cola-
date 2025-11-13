from django.contrib import admin
from .models import Pedido, Cliente, Producto

admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Pedido)
