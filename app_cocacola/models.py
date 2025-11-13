from django.db import models
from datetime import date
from django.utils import timezone

# ==========================================
# MODELO: CLIENTE
# ==========================================
class Cliente(models.Model):
    # Datos personales
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True, null=True)  # opcional
    # Contacto / dirección
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    # Preferencias y sistema
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    preferencia = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================================
# MODELO: PRODUCTO
# ==========================================
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()
    fecha_fabricacion = models.DateField(default=date.today)
    fecha_vencimiento = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre_producto



# -------------------------
# MODELO: PEDIDO (tercera parte)
# -------------------------
class Pedido(models.Model):
    # opciones
    METODO_PAGO_CHOICES = [
        ("Efectivo", "Efectivo"),
        ("Tarjeta", "Tarjeta"),
        ("Transferencia", "Transferencia"),
    ]
    ESTADO_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Enviado", "Enviado"),
        ("Entregado", "Entregado"),
        ("Cancelado", "Cancelado"),
    ]

    numero_pedido = models.CharField(max_length=30, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, blank=True)
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    direccion_envio = models.CharField(max_length=255, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default="Efectivo")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")
    observaciones = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # MANUAL: rellenado por el usuario

    def __str__(self):
        return f"{self.numero_pedido} - {self.cliente.nombre} {self.cliente.apellido}"