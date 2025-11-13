from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Cliente, Producto, Pedido 
from django.utils.crypto import get_random_string
from decimal import Decimal
from django.utils import timezone

# Vista inicio
def inicio_cocacola(request):
    # información general para la página de inicio
    total_clientes = Cliente.objects.count()
    clientes_recientes = Cliente.objects.order_by('-fecha_registro')[:5]
    context = {
        'total_clientes': total_clientes,
        'clientes_recientes': clientes_recientes,
    }
    return render(request, 'inicio.html', context)


# Agregar cliente (muestra formulario HTML simple - sin forms.py)
def agregar_cliente(request):
    if request.method == 'POST':
        # sin validación: obtener directamente del POST
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        preferencia = request.POST.get('preferencia', '')
        # campos opcionales
        ciudad = request.POST.get('ciudad', '')
        estado = request.POST.get('estado', '')
        codigo_postal = request.POST.get('codigo_postal', '')
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None

        cliente = Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono,
            email=email,
            preferencia=preferencia,
            ciudad=ciudad or None,
            estado=estado or None,
            codigo_postal=codigo_postal or None,
            fecha_nacimiento=fecha_nacimiento or None
        )
        # redirigir a ver clientes
        return redirect('ver_cliente')
    return render(request, 'cliente/agregar_cliente.html')


# Mostrar clientes
def ver_cliente(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    context = {'clientes': clientes}
    return render(request, 'cliente/ver_cliente.html', context)


# Mostrar formulario para actualizar (GET)
def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    context = {'cliente': cliente}
    return render(request, 'cliente/actualizar_cliente.html', context)


# Recibe POST con la actualización y la guarda
def realizar_actualizacion_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre', cliente.nombre)
        cliente.apellido = request.POST.get('apellido', cliente.apellido)
        cliente.direccion = request.POST.get('direccion', cliente.direccion)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.email = request.POST.get('email', cliente.email)
        cliente.preferencia = request.POST.get('preferencia', cliente.preferencia)
        cliente.ciudad = request.POST.get('ciudad', cliente.ciudad)
        cliente.estado = request.POST.get('estado', cliente.estado)
        cliente.codigo_postal = request.POST.get('codigo_postal', cliente.codigo_postal)
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        if fecha_nacimiento:
            cliente.fecha_nacimiento = fecha_nacimiento
        cliente.save()
        return redirect('ver_cliente')
    # si no es POST, redirigir al editar
    return redirect('actualizar_cliente', cliente_id=cliente.id)


# Borrar cliente (confirmación GET, confirmación POST borra)
def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_cliente')
    context = {'cliente': cliente}
    return render(request, 'cliente/borrar_cliente.html', context)


# ===============================
# AGREGAR PRODUCTO
# ===============================
def agregar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        categoria = request.POST.get('categoria')
        precio_unitario = request.POST.get('precio_unitario')
        stock_actual = request.POST.get('stock_actual')
        fecha_fabricacion = request.POST.get('fecha_fabricacion')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        Producto.objects.create(
            nombre_producto=nombre_producto,
            categoria=categoria,
            precio_unitario=precio_unitario,
            stock_actual=stock_actual,
            fecha_fabricacion=fecha_fabricacion,
            fecha_vencimiento=fecha_vencimiento
        )
        return redirect('ver_producto')

    return render(request, 'producto/agregar_producto.html')


# ===============================
# VER PRODUCTO
# ===============================
def ver_producto(request):
    productos = Producto.objects.all()
    return render(request, 'producto/ver_producto.html', {'productos': productos})


# ===============================
# ACTUALIZAR PRODUCTO
# ===============================
def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'producto/actualizar_producto.html', {'producto': producto})


# ===============================
# REALIZAR ACTUALIZACIÓN
# ===============================
def realizar_actualizacion_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.categoria = request.POST.get('categoria')
        producto.precio_unitario = request.POST.get('precio_unitario')
        producto.stock_actual = request.POST.get('stock_actual')
        producto.fecha_fabricacion = request.POST.get('fecha_fabricacion')
        producto.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        producto.save()
        return redirect('ver_producto')


# ===============================
# BORRAR PRODUCTO
# ===============================
def borrar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_producto')
    return render(request, 'producto/borrar_producto.html', {'producto': producto})


# GENERADOR simple de número de pedido
def generar_numero_pedido():
    pref = timezone.now().strftime('%Y%m%d')
    suf = get_random_string(4, allowed_chars='0123456789')
    return f"{pref}-{suf}"

# ===============================
# VER PRODUCTO
# ===============================
def ver_producto(request):
    productos = Producto.objects.all()
    return render(request, 'producto/ver_producto.html', {'productos': productos})


# ===============================
# ACTUALIZAR PRODUCTO
# ===============================
def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'producto/actualizar_producto.html', {'producto': producto})


# ===============================
# REALIZAR ACTUALIZACIÓN
# ===============================
def realizar_actualizacion_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.categoria = request.POST.get('categoria')
        producto.precio_unitario = Decimal(request.POST.get('precio_unitario') or '0.00')
        producto.stock_actual = request.POST.get('stock_actual')
        producto.fecha_fabricacion = request.POST.get('fecha_fabricacion')
        producto.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        producto.save()
        return redirect('ver_producto')


# ===============================
# BORRAR PRODUCTO
# ===============================
def borrar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_producto')
    return render(request, 'producto/borrar_producto.html', {'producto': producto})


# ---- AGREGAR PEDIDO ----
def agregar_pedido(request):
    clientes = Cliente.objects.all().order_by('nombre')
    productos = Producto.objects.all().order_by('nombre_producto')


    if request.method == "POST":
        numero_pedido = request.POST.get("numero_pedido", "").strip()
        cliente_id = request.POST.get("cliente")
        productos_ids = request.POST.getlist("productos")  # lista de ids
        fecha_entrega = request.POST.get("fecha_entrega") or None
        direccion_envio = request.POST.get("direccion_envio", "")
        metodo_pago = request.POST.get("metodo_pago", "Efectivo")
        estado = request.POST.get("estado", "Pendiente")
        observaciones = request.POST.get("observaciones", "")
        total_str = request.POST.get("total", "0").strip()

        # convertir total sin validacion robusta (según tu requerimiento)
        try:
            total = Decimal(total_str)
        except Exception:
            total = Decimal('0.00')

        cliente = get_object_or_404(Cliente, id=cliente_id) if cliente_id else None

        pedido = Pedido.objects.create(
            numero_pedido=numero_pedido,
            cliente=cliente,
            fecha_entrega=fecha_entrega or None,
            direccion_envio=direccion_envio,
            metodo_pago=metodo_pago,
            estado=estado,
            observaciones=observaciones,
            total=total
        )

        # asignar productos many-to-many
        if productos_ids:
            pedido.productos.set(productos_ids)

        return redirect("ver_pedido")

    return render(request, "pedido/agregar_pedido.html", {
        "clientes": clientes,
        "productos": productos
    })


# ---- VER LISTA DE PEDIDOS ----
def ver_pedido(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido', '-id')
    return render(request, "pedido/ver_pedido.html", {"pedidos": pedidos})


# ---- MOSTRAR DETALLE ----
def mostrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "pedido/mostrar_pedido.html", {"pedido": pedido})


# ---- ACTUALIZAR (mostrar form) ----
def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    clientes = Cliente.objects.all().order_by('nombre')
    productos = Producto.objects.all().order_by('nombre_producto')

    # form apunta a realizar_actualizacion_pedido
    return render(request, "pedido/actualizar_pedido.html", {
        "pedido": pedido,
        "clientes": clientes,
        "productos": productos
    })


# ---- GUARDAR ACTUALIZACIÓN (POST) ----
def realizar_actualizacion_pedido(request, pedido_id):
    if request.method != "POST":
        return redirect("ver_pedido")

    pedido = get_object_or_404(Pedido, id=pedido_id)

    pedido.numero_pedido = request.POST.get("numero_pedido", pedido.numero_pedido).strip()
    cliente_id = request.POST.get("cliente")
    productos_ids = request.POST.getlist("productos")
    pedido.fecha_entrega = request.POST.get("fecha_entrega") or None
    pedido.direccion_envio = request.POST.get("direccion_envio", pedido.direccion_envio)
    pedido.metodo_pago = request.POST.get("metodo_pago", pedido.metodo_pago)
    pedido.estado = request.POST.get("estado", pedido.estado)
    pedido.observaciones = request.POST.get("observaciones", pedido.observaciones)
    total_str = request.POST.get("total", str(pedido.total)).strip()

    try:
        pedido.total = Decimal(total_str)
    except Exception:
        # si falla, no cambiar
        pass

    if cliente_id:
        pedido.cliente = get_object_or_404(Cliente, id=cliente_id)

    pedido.save()

    # actualizar M2M
    if productos_ids:
        pedido.productos.set(productos_ids)
    else:
        pedido.productos.clear()

    return redirect("ver_pedido")


# ---- BORRAR PEDIDO ----
def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == "POST":
        pedido.delete()
        return redirect("ver_pedido")
    return render(request, "pedido/borrar_pedido.html", {"pedido": pedido})