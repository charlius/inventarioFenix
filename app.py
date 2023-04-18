import json
from werkzeug.security import check_password_hash
from flask import Flask, jsonify, render_template, request, redirect, session
from src.gestion_inventario_db import Bodega, Movimiento, Producto, Proveedor, Usuario



app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
  return render_template('index.html')


def verificar_password(password, password_hash):
    return check_password_hash(password_hash, password)


@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  usuario = Usuario.obtener_por_email(username)
  if usuario and verificar_password(password, usuario.contrasena):
    print("correcta las credenciales..!")
    session['usuario'] = usuario.nombre_usuario
    return redirect('/dashboard')
  else:
    return render_template('index.html', mensaje='Correo electrónico o contraseña incorrectos')


@app.route('/dashboard')
def dashboard():
  if 'usuario' in session:
    usuario = Usuario.obtener_por_email(session['usuario'])
    list_producto = []
    producto = Producto.traer_stock_minimo()
    for prod in producto:
       print(prod)
       list_producto.append(list(prod))
       print(list_producto)
    return render_template('dashboard.html', usuario=usuario, productos=list_producto)
  else:
    return redirect('/')


@app.route('/logout')
def logout():
  session.pop('usuario', None)
  return redirect('/')


# @app.route('/usuarios')
# def usuarios():
#   if 'usuario' in session:
#     usuario = Usuario.obtener_por_email(session['usuario'])
#     if usuario.tipo_usuario:
#       lista_usuarios = Usuario.obtener_todos()
#       return render_template('usuario.html', usuario=usuario, lista_usuarios=lista_usuarios)
#     else:
#       return redirect('/dashboard')
#   else:
#     return redirect('/')


@app.route('/productos')
def productos():
    if 'usuario' in session:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()

        # incluir variable en la respuesta
        return render_template('productos.html', usuario=usuario, productos=productos)
    else:
        return redirect('/')


@app.route('/productos/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if 'usuario' not in session:
        return redirect('/')
    if request.method == 'POST':
        print("entro al post")
        print(request.form['nombre'])
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        proveedor_id = request.form['proveedor_id']
        id_bodega = request.form['bodega_id']
        cantidad = request.form['existencia']
        cantidad_minima = request.form['cantidad_minima']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        nuevo_producto = Producto(
           nombre_producto=nombre,
           descripcion=descripcion,
           precio_compra=precio_compra,
           precio_venta=precio_venta,
           cantidad=cantidad,
           cantidad_minima=cantidad_minima,
           proveedor_id=proveedor_id,
           id_bodega=id_bodega
        )
        nuevo_producto.guardar()
        return redirect('/productos')
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('crear_producto.html', proveedores=proveedores, bodegas=bodegas)


@app.route('/productos/<int:producto_id>/editar', methods=['GET', 'POST'])
def editar_producto(producto_id=0):
    if 'usuario' not in session:
        return redirect('/')
    producto = Producto.obtener_por_id(producto_id)
    if not producto:
        return redirect('/productos')
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        proveedor_id = request.form['proveedor_id']
        id_bodega = request.form['bodega_id']
        cantidad = request.form['existencia']
        cantidad_minima = request.form['cantidad_minima']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']

        producto_edit = Producto(
           nombre_producto=nombre,
           descripcion=descripcion,
           precio_compra=precio_compra,
           precio_venta=precio_venta,
           cantidad=cantidad,
           cantidad_minima=cantidad_minima,
           proveedor_id=proveedor_id,
           id_bodega=id_bodega
        )
        producto_edit.id = producto_id
        print(producto_edit.id)

        producto_edit.editar()
        return redirect('/productos')
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('editar_producto.html', producto=producto, proveedores=proveedores, bodegas=bodegas)


@app.route('/filtrar', methods=['GET'])
def traer_stock_minimo():
    if 'usuario' not in session:
        return redirect('/')
    list_producto = []
    producto = Producto.traer_stock_minimo()
    for prod in producto:
       print(prod)
       list_producto.append(list(prod))
       print(list_producto)
        
    return render_template('productos_stock_minimo.html', productos=list_producto)


@app.route('/proveedores')
def proveedores():
  if 'usuario' not in session:
        return redirect('/')
  proveedores = Proveedor.obtener_todos()
  print(str(proveedores[0].nombre_proveedor))
  return render_template('proveedor.html', proveedores=proveedores)

@app.route('/proveedores/<int:proveedor_id>/editar', methods=['GET', 'POST'])
def editar_proveedor(proveedor_id=0):
    if 'usuario' not in session:
        return redirect('/')
    proveedor = Proveedor.obtener_por_id(proveedor_id)
    if not proveedor:
        return redirect('/proveedores')
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        proveedor_edit = Proveedor(
           nombre_proveedor=nombre,
           direccion=direccion,
           telefono=telefono
        )
        proveedor_edit.id = proveedor_id
        print(proveedor_edit.id)

        proveedor_edit.editar()
        return redirect('/proveedores')
    return render_template('editar_proveedor.html', proveedor=proveedor)

@app.route('/proveedores/crear_proveedor', methods=['GET', 'POST'])
def crear_proveedor():
    if 'usuario' not in session:
        return redirect('/')
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        nuevo_proveedor = Proveedor(
           nombre_proveedor=nombre,
           direccion=direccion,
           telefono=telefono
        )


        nuevo_proveedor.guardar()
        return redirect('/proveedores')
    return render_template('crear_proveedor.html')


@app.route('/bodegas')
def bodegas():
    if 'usuario' in session:
        usuario = Usuario.obtener_por_email(session['usuario'])
        bodegas = Bodega.obtener_todos()

        # incluir variable en la respuesta
        return render_template('bodega.html', usuario=usuario, bodegas=bodegas)
    else:
        return redirect('/')
    
@app.route('/bodega/crear_bodega', methods=['GET', 'POST'])
def crear_bodega():
    if 'usuario' not in session:
        return redirect('/')
    if request.method == 'POST':
        print("hola")
        nombre_bodega = request.form['nombre_bodega']
        direccion = request.form['direccion']
        
        nueva_bodega = Bodega(
           nombre_bodega=nombre_bodega,
           direccion=direccion
          )
        nueva_bodega.guardar()
        return redirect('/bodegas')
    return render_template('crear_bodega.html')

@app.route('/bodegas/<int:bodega_id>/editar', methods=['GET', 'POST'])
def editar_bodega(bodega_id=0):
    if 'usuario' not in session:
        return redirect('/')
    bodega = Bodega.obtener_por_id(bodega_id)
    if not bodega:
        return redirect('/bodegas')
    if request.method == 'POST':
        nombre = request.form['nombre_bodega']
        direccion = request.form['direccion']

        bodega_edit = Bodega(
           nombre_bodega=nombre,
           direccion=direccion
        )
        bodega_edit.id = bodega_id
        print(bodega_edit.id)

        bodega_edit.editar()
        return redirect('/bodegas')
    return render_template('editar_bodega.html', bodega=bodega)

@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect('/')

        # incluir variable en la respuesta
    usuarios = Usuario.obtener_todos()
    print(usuarios[0].nombre_usuario)
    return render_template('usuario.html', usuarios=usuarios)

@app.route('/usuario/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if 'usuario' not in session:
        return redirect('/')
    if request.method == 'POST':
        print(f"hola: {request.form}")
        nombre_usuario = request.form['nombre_usuario']
        password = request.form['password']
        tipo_usuario = request.form['rol']

        nueva_usuario = Usuario(
           nombre_usuario=nombre_usuario,
           contrasena=password,
           tipo_usuario=tipo_usuario
        )
        nueva_usuario.guardar()
        return redirect('/usuarios')
    return render_template('crear_usuario.html')

@app.route('/usuario/<id>/editar', methods=['GET', 'POST'])
def editar_usuario(id=0):
    print(f"este es id = {id}")
    if 'usuario' not in session:
        return redirect('/')
    usuario = Usuario.obtener_por_id(id)

    if not usuario:
        return redirect('/usuarios')
    print(request.method)
    if request.method == 'POST':
        print(request.form)
        nombre_usuario = request.form['nombre_usuario']
        password = request.form['password']
        tipo_usuario = request.form['rol']
        usuario_edit = Usuario(
           nombre_usuario=nombre_usuario,
           contrasena=password,
           tipo_usuario=tipo_usuario
        )
        usuario_edit.id = id
        print(usuario_edit.id)

        usuario_edit.editar()
        return redirect('/usuarios')
    print("vee")
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    if request.method == 'POST':
        print(print(request.form))
        tipo = request.form['tipo_movimiento']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form["fecha_fin"]

        if "todo" in tipo:
            movimientos = Movimiento.obtener_todos()
        elif fecha_fin and fecha_fin:
            movimientos = Movimiento.obtener_por_tipo_movimiento_rango_fecha(tipo, fecha_inicio, fecha_fin)
        else:
            movimientos = Movimiento.obtener_por_tipo_movimiento(tipo)
        # Convertir cada objeto en un diccionario y agregarlo a una lista
        movimientos_dict = []
        for movimiento in movimientos:
            del movimiento.conexion_db
            movimiento_dict = movimiento.__dict__
            movimientos_dict.append(movimiento_dict)

        print(movimientos_dict)
        # Serializar la lista de diccionarios en formato JSON
        json_movimientos = json.dumps(movimientos_dict)
        return json_movimientos
    return render_template('movimientos.html')

app.route('/movimientos/buscar', methods=['GET', 'POST'])
def buscar_movimientos():
    if request.method == 'POST':
        print(print(request.form))
    return render_template('movimientos.html')

@app.route('/entrada')
def entrada():
    if 'usuario' in session:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()

        # incluir variable en la respuesta
        return render_template('entrada.html', usuario=usuario, productos=productos)
    else:
        return redirect('/')
    
@app.route('/productos/<int:producto_id>/ajustar_cantidad', methods=['GET', 'POST'])
def ajustar_producto(producto_id=0):
    if 'usuario' not in session:
        return redirect('/')
    producto = Producto.obtener_por_id(producto_id)
    if not producto:
        return redirect('/productos')
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        proveedor_id = request.form['proveedor_id']
        id_bodega = request.form['bodega_id']
        cantidad = request.form['existencia']
        cantidad_minima = request.form['cantidad_minima']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']

        producto_edit = Producto(
           nombre_producto=nombre,
           descripcion=descripcion,
           precio_compra=precio_compra,
           precio_venta=precio_venta,
           cantidad=cantidad,
           cantidad_minima=cantidad_minima,
           proveedor_id=proveedor_id,
           id_bodega=id_bodega
        )
        producto_edit.id = producto_id
        print(producto_edit.id)

        producto_edit.editar()
        return redirect('/productos')
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('ajustar_producto.html', producto=producto, proveedores=proveedores, bodegas=bodegas)

@app.route('/salida')
def salida():
    if 'usuario' in session:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()

        # incluir variable en la respuesta
        return render_template('salida.html', usuario=usuario, productos=productos)
    else:
        return redirect('/')
    
@app.route('/productos/<int:producto_id>/salida_producto', methods=['GET', 'POST'])
def ajustar_salida(producto_id=0):
    if 'usuario' not in session:
        return redirect('/')
    producto = Producto.obtener_por_id(producto_id)
    if not producto:
        return redirect('/productos')
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        proveedor_id = request.form['proveedor_id']
        id_bodega = request.form['bodega_id']
        cantidad = request.form['existencia']
        cantidad_minima = request.form['cantidad_minima']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']

        producto_edit = Producto(
           nombre_producto=nombre,
           descripcion=descripcion,
           precio_compra=precio_compra,
           precio_venta=precio_venta,
           cantidad=cantidad,
           cantidad_minima=cantidad_minima,
           proveedor_id=proveedor_id,
           id_bodega=id_bodega
        )
        producto_edit.id = producto_id
        print(producto_edit.id)

        producto_edit.editar()
        return redirect('/productos')
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('ajustar_salida.html', producto=producto, proveedores=proveedores, bodegas=bodegas)

# #####################################3



if __name__ == '__main__':
    app.run(debug=True)
