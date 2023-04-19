import json
from werkzeug.security import check_password_hash
from flask import Flask, jsonify, render_template, request, redirect, session
from src.gestion_inventario_db import Bodega, Categoria, Movimiento, Producto, Proveedor, Usuario



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
    session['tipo_usuario'] = usuario.tipo_usuario
    session['nombre_usuario'] = usuario.nombre_usuario
    return redirect('/dashboard')
  else:
    return render_template('index.html', mensaje='Correo electrónico o contraseña incorrectos')




@app.route('/dashboard')
def dashboard():
  if 'usuario' in session:
    usuario = Usuario.obtener_por_email(session['usuario'])
    print(usuario.tipo_usuario)
    list_producto = []
    producto = Producto.traer_stock_minimo()
    for prod in producto:
       list_producto.append(list(prod))
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
    if 'usuario' in session and "administrador" in session['tipo_usuario']:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()

        # incluir variable en la respuesta
        return render_template('productos.html', usuario=usuario, productos=productos)
    else:
        return redirect('/')


@app.route('/productos/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    if request.method == 'POST':
        usuario = Usuario.obtener_por_email(session['usuario'])
        print(request.form)
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        proveedor_id = request.form['proveedor_id']
        id_bodega = request.form['bodega_id']
        cantidad = request.form['existencia']
        cantidad_minima = request.form['cantidad_minima']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        id_categoria = request.form['categoria_id']
        nuevo_producto = Producto(
           nombre_producto=nombre,
           descripcion=descripcion,
           precio_compra=precio_compra,
           precio_venta=precio_venta,
           cantidad=cantidad,
           cantidad_minima=cantidad_minima,
           proveedor_id=proveedor_id,
           id_bodega=id_bodega,
           categoria_id=id_categoria
        )
        nuevo_producto.guardar(usuario.id)
        return redirect('/productos')
    categorias = Categoria.obtener_todos()
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('crear_producto.html', proveedores=proveedores, bodegas=bodegas, categorias=categorias)


@app.route('/productos/<int:producto_id>/editar', methods=['GET', 'POST'])
def editar_producto(producto_id=0):
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    producto = Producto.obtener_por_id(producto_id)
    usuario = Usuario.obtener_por_email(session['usuario'])
    if not producto:
        return redirect('/productos')
    if request.method == 'POST':
        if request.form.get('nombre', ""):
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            proveedor_id = request.form['proveedor_id']
            id_bodega = request.form['bodega_id']
            cantidad = request.form['existencia']
            cantidad_minima = request.form['cantidad_minima']
            precio_compra = request.form['precio_compra']
            precio_venta = request.form['precio_venta']
            categoria_id = request.form['categoria_id']

            producto_edit = Producto(
            nombre_producto=nombre,
            descripcion=descripcion,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            cantidad=cantidad,
            cantidad_minima=cantidad_minima,
            proveedor_id=proveedor_id,
            id_bodega=id_bodega,
            categoria_id=categoria_id
            )
            producto_edit.id = producto_id

            producto_edit.editar()
            return redirect('/productos')
        data = json.loads(request.data)
        movimiento = data.get('movimiento', "")
        if movimiento:
            if not producto:
                return redirect('/salida')
            cantidad = data['new_existencia']
            if "salida" in movimiento:
                producto.cantidad = producto.cantidad - int(cantidad)
            elif "entrada" in movimiento:
                producto.cantidad = producto.cantidad + int(cantidad)

            producto.editar_movimiento(int(cantidad), movimiento, usuario.id)
            return {"message": "ok"}

    categorias = Categoria.obtener_todos()
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('editar_producto.html', producto=producto, proveedores=proveedores, bodegas=bodegas, categorias=categorias)


@app.route('/filtrar', methods=['GET'])
def traer_stock_minimo():
    if 'usuario' not in session:
        return redirect('/')
    list_producto = []
    producto = Producto.traer_stock_minimo()
    for prod in producto:
       list_producto.append(list(prod))
        
    return render_template('productos_stock_minimo.html', productos=list_producto)


@app.route('/proveedores')
def proveedores():
  if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
  proveedores = Proveedor.obtener_todos()
  return render_template('proveedor.html', proveedores=proveedores)

@app.route('/proveedores/<int:proveedor_id>/editar', methods=['GET', 'POST'])
def editar_proveedor(proveedor_id=0):
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
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

        proveedor_edit.editar()
        return redirect('/proveedores')
    return render_template('editar_proveedor.html', proveedor=proveedor)

@app.route('/proveedores/crear_proveedor', methods=['GET', 'POST'])
def crear_proveedor():
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
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

@app.route('/categorias')
def categorias():
    if 'usuario' in session and "administrador" in session['tipo_usuario']:
        usuario = Usuario.obtener_por_email(session['usuario'])
        categorias = Categoria.obtener_todos()

        # incluir variable en la respuesta
        return render_template('categorias.html', usuario=usuario, categorias=categorias)
    else:
        return redirect('/')

@app.route('/categoria/crear_categoria', methods=['GET', 'POST'])
def crear_categoria():
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']

        nueva_categoria = Categoria(
           nombre=nombre_categoria
          )
        nueva_categoria.guardar()
        return redirect('/categorias')
    return render_template('crear_categorias.html')

@app.route('/categorias/<int:categoria_id>/editar', methods=['GET', 'POST'])
def editar_categorias(categoria_id=0):
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    categoria = Categoria.obtener_por_id(categoria_id)
    if not categoria:
        return redirect('/categorias')
    if request.method == 'POST':
        nombre = request.form['nombre_categoria']

        categoria_edit = Categoria(
           nombre=nombre
        )
        categoria_edit.id = categoria_id

        categoria_edit.editar()
        return redirect('/categorias')
    return render_template('editar_categorias.html', categoria=categoria)

@app.route('/bodegas')
def bodegas():
    if 'usuario' in session and "administrador" in session['tipo_usuario']:
        usuario = Usuario.obtener_por_email(session['usuario'])
        bodegas = Bodega.obtener_todos()

        # incluir variable en la respuesta
        return render_template('bodega.html', usuario=usuario, bodegas=bodegas)
    else:
        return redirect('/')
    
@app.route('/bodega/crear_bodega', methods=['GET', 'POST'])
def crear_bodega():
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    if request.method == 'POST':
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
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
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

        bodega_edit.editar()
        return redirect('/bodegas')
    return render_template('editar_bodega.html', bodega=bodega)

@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')

        # incluir variable en la respuesta
    usuarios = Usuario.obtener_todos()
    return render_template('usuario.html', usuarios=usuarios)

@app.route('/usuario/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    if request.method == 'POST':
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
    if 'usuario' not in session and "administrador" not in session['tipo_usuario']:
        return redirect('/')
    usuario = Usuario.obtener_por_id(id)

    if not usuario:
        return redirect('/usuarios')
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        password = request.form['password']
        tipo_usuario = request.form['rol']
        usuario_edit = Usuario(
           nombre_usuario=nombre_usuario,
           contrasena=password,
           tipo_usuario=tipo_usuario
        )
        usuario_edit.id = id

        usuario_edit.editar()
        return redirect('/usuarios')
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    if request.method == 'POST':
        print(request.form)
        tipo = request.form['tipo_movimiento']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form["fecha_fin"]
        nombre_producto = request.form["nombre_producto"]

        if "todo" in tipo and nombre_producto and fecha_fin and fecha_fin:
            movimientos = Movimiento.obtener_todos_nombre_rango_fecha(nombre_producto, fecha_inicio, fecha_fin)
        elif "todo" in tipo and fecha_fin and fecha_fin:
            movimientos = Movimiento.obtener_todos_rango_fecha(fecha_inicio, fecha_fin)
        elif "todo" in tipo and nombre_producto:
            movimientos = Movimiento.obtener_todos_nombre(nombre_producto)
        elif "todo" in tipo:
            movimientos = Movimiento.obtener_todos()
        elif nombre_producto and fecha_fin and fecha_fin:
             movimientos = Movimiento.obtener_por_tipo_movimiento_rango_fecha_nombre_producto(
                tipo, fecha_inicio, fecha_fin, nombre_producto
            )

        elif fecha_fin and fecha_fin:
           movimientos = Movimiento.obtener_por_tipo_movimiento_rango_fecha(tipo, fecha_inicio, fecha_fin)
        elif nombre_producto:
            movimientos = Movimiento.obtener_por_tipo_movimiento_nombre_producto(tipo, nombre_producto)
        else:
            movimientos = Movimiento.obtener_por_tipo_movimiento(tipo)
        # Convertir cada objeto en un diccionario y agregarlo a una lista
        movimientos_dict = []
        for movimiento in movimientos:
            del movimiento.conexion_db
            movimiento_dict = movimiento.__dict__
            movimientos_dict.append(movimiento_dict)

        # Serializar la lista de diccionarios en formato JSON
        json_movimientos = json.dumps(movimientos_dict)
        return json_movimientos
    return render_template('movimientos.html')

app.route('/movimientos/buscar', methods=['GET', 'POST'])
def buscar_movimientos():
    return render_template('movimientos.html')

@app.route('/entrada')
def entrada():
    if 'usuario' in session and "administrador" in session['tipo_usuario']:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()

        # incluir variable en la respuesta
        return render_template('entrada.html', usuario=usuario, productos=productos)
    else:
        return redirect('/')
    
@app.route('/productos/<int:producto_id>/ajustar_cantidad', methods=['GET', 'POST'])
def ajustar_producto(producto_id=0):
    if 'usuario' not in session :
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
        return render_template('ajustar_salida.html')
    else:
        return redirect('/')
    
@app.route('/entradas')
def entradas():
    if 'usuario' in session and "administrador" in session['tipo_usuario']:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()

        # incluir variable en la respuesta
        return render_template('ajustar_entradas.html')
    else:
        return redirect('/')

@app.route('/buscar_nombre', methods=['GET', 'POST'])
def buscar_nombre():
    if 'usuario' in session:
        usuario = Usuario.obtener_por_email(session['usuario'])
        productos = Producto.obtener_todos()
        if request.method == 'POST':
            nombre = request.form['buscar_nombre']
            producto = Producto.obtener_por_nombre(nombre)
            if producto:
                producto_dict = {
                    'id': producto.id,
                    'nombre': producto.nombre_producto,
                    'descripcion': producto.descripcion,
                    'cantidad': producto.cantidad
                    # agrega los demás atributos del objeto Producto aquí
                }
                return producto_dict
            return {}
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
    return render_template('ajustar_salida_stock_minimo.html', producto=producto, proveedores=proveedores, bodegas=bodegas)

# #####################################3



if __name__ == '__main__':
    app.run(debug=True)
