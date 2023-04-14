from werkzeug.security import check_password_hash
from flask import Flask, jsonify, render_template, request, redirect, session
from src.gestion_inventario_db import Bodega, Producto, Proveedor, Usuario



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
    return render_template('dashboard.html', usuario=usuario)
  else:
    return redirect('/')


@app.route('/logout')
def logout():
  session.pop('usuario', None)
  return redirect('/')


@app.route('/usuarios')
def usuarios():
  if 'usuario' in session:
    usuario = Usuario.obtener_por_email(session['usuario'])
    if usuario.tipo_usuario:
      lista_usuarios = Usuario.obtener_todos()
      return render_template('usuario.html', usuario=usuario, lista_usuarios=lista_usuarios)
    else:
      return redirect('/dashboard')
  else:
    return redirect('/')


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
    proveedores = Proveedor.obtener_todos()
    bodegas = Bodega.obtener_todos()
    return render_template('crear_bodega.html')




@app.route('/movimientos')
def movimientos():
    return render_template('movimientos.html')
    

if __name__ == '__main__':
    app.run(debug=True)
