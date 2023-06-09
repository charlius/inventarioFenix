

from datetime import datetime
from werkzeug.security import generate_password_hash
from src.db import ConexionBaseDatos


class Proveedor:
  def __init__(self, nombre_proveedor, direccion, telefono):
    self.conexion_db = ConexionBaseDatos()
    self.id = None
    self.nombre_proveedor = nombre_proveedor
    self.direccion = direccion
    self.telefono = telefono

  def guardar(self):
    consulta = "INSERT INTO proveedores (nombre_proveedor, direccion, telefono) VALUES (%s, %s, %s)"
    valores = (self.nombre_proveedor, self.direccion, self.telefono)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  def editar(self):
    consulta = "UPDATE proveedores SET nombre_proveedor=%s, direccion=%s, telefono=%s WHERE id=%s"
    valores = (self.nombre_proveedor, self.direccion, self.telefono, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  @staticmethod
  def obtener_todos():
    consulta = "SELECT * FROM proveedores"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    proveedores = []
    for resultado in resultados:
      proveedor = Proveedor(resultado[1], resultado[2], resultado[3])
      proveedor.id = resultado[0]
      proveedores.append(proveedor)
    return proveedores

  @staticmethod
  def obtener_por_id(id):
    consulta = "SELECT * FROM proveedores WHERE id=%s"
    valores = (id,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    proveedor = None
    if len(resultado) > 0:
      proveedor = Proveedor(resultado[0][1], resultado[0][2], resultado[0][3])
      proveedor.id = resultado[0][0]
    return proveedor


class Producto:
  def __init__(
      self,
      nombre_producto="",
      descripcion="",
      precio_compra=0,
      precio_venta=0,
      cantidad=0,
      cantidad_minima=0,
      proveedor_id=0,
      id_bodega=0,
      categoria_id=0
):
    self.conexion_db = ConexionBaseDatos()
    self.id = None
    self.nombre_producto = nombre_producto
    self.descripcion = descripcion
    self.precio_compra = precio_compra
    self.precio_venta = precio_venta
    self.cantidad = cantidad
    self.cantidad_minima = cantidad_minima
    self.proveedor_id = proveedor_id
    self.id_bodega = id_bodega
    self.id_categoria = categoria_id

  def guardar(self, id_usuario, code_qr):
    consulta = "INSERT INTO productos (nombre_producto, descripcion, precio_compra, precio_venta, cantidad, cantidad_minima, proveedor_id, id_bodega, id_categoria, code_qr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
    valores = (self.nombre_producto, self.descripcion, self.precio_compra, self.precio_venta, self.cantidad, self.cantidad_minima, self.proveedor_id, self.id_bodega, self.id_categoria, code_qr)
    self.conexion_db.ejecutar_consulta(consulta, valores)
    product = Producto.obtener_por_nombre(self.nombre_producto)
    print(f"product--- {product.id}")
    Movimiento(product.id, self.id_bodega, self.cantidad, "entrada", id_usuario).guardar()

  def editar(self):
    consulta = "UPDATE productos SET nombre_producto=%s, descripcion=%s, precio_compra=%s, precio_venta=%s, cantidad=%s, cantidad_minima=%s, proveedor_id=%s, id_bodega=%s, id_categoria=%s WHERE id=%s"
    valores = (self.nombre_producto, self.descripcion, self.precio_compra, self.precio_venta, self.cantidad, self.cantidad_minima, self.proveedor_id, self.id_bodega, self.id_categoria, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  def editar_movimiento(self, cantidad, movimiento, id_usuario):
    consulta = "UPDATE productos SET nombre_producto=%s, descripcion=%s, precio_compra=%s, precio_venta=%s, cantidad=%s, cantidad_minima=%s, proveedor_id=%s, id_bodega=%s, id_categoria=%s WHERE id=%s"
    valores = (self.nombre_producto, self.descripcion, self.precio_compra, self.precio_venta, self.cantidad, self.cantidad_minima, self.proveedor_id, self.id_bodega, self.id_categoria, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)
    Movimiento(self.id, self.id_bodega, cantidad, movimiento, id_usuario).guardar()


  

  @staticmethod
  def obtener_todos():
    consulta = "SELECT * FROM productos"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    productos = []
    for resultado in resultados:
      producto = Producto(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
      producto.id = resultado[0]
      productos.append(producto)
    return productos
  

  @staticmethod
  def obtener_por_id(id):
    consulta = "SELECT * FROM productos WHERE id=%s"
    valores = (id,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    producto = None
    if len(resultado) > 0:
      producto = Producto(resultado[0][1], resultado[0][2], resultado[0][3], resultado[0][4], resultado[0][5], resultado[0][6],resultado[0][7],resultado[0][8],resultado[0][9])
      producto.id = resultado[0][0]
    return producto

  @staticmethod
  def obtener_por_nombre(nombre):
    consulta = "SELECT * FROM productos WHERE nombre_producto=%s"
    valores = (nombre,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    producto = None
    if len(resultado) > 0:
      producto = Producto(resultado[0][1], resultado[0][2], resultado[0][3], resultado[0][4], resultado[0][5], resultado[0][6],resultado[0][7],resultado[0][8],resultado[0][9])
      producto.id = resultado[0][0]
    return producto

  @staticmethod
  def traer_stock_minimo():
    consulta = "SELECT * FROM productos WHERE cantidad <= cantidad_minima"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    productos = []
    for resultado in resultados:
      producto = Producto(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
      productos.append(producto)
    return resultados

  @staticmethod
  def obtener_productos_por_categoria(id_categoria):
    consulta =f"SELECT * FROM productos WHERE id_categoria = {id_categoria}"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    productos = []
    for resultado in resultados:
      producto = Producto(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
      producto.id = resultado[0]
      
      productos.append(resultado[1])
    return productos

class Bodega:
  def __init__(self, nombre_bodega, direccion):
    self.conexion_db = ConexionBaseDatos()
    self.id = None
    self.nombre_bodega = nombre_bodega
    self.direccion = direccion

  def guardar(self):
    consulta = "INSERT INTO bodegas (nombre_bodega, direccion) VALUES (%s, %s)"
    valores = (self.nombre_bodega, self.direccion)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  def editar(self):
    consulta = "UPDATE bodegas SET nombre_bodega=%s, direccion=%s WHERE id=%s"
    valores = (self.nombre_bodega, self.direccion, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  @staticmethod
  def obtener_todos():
    consulta = "SELECT * FROM bodegas"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    bodegas = []
    for resultado in resultados:
      bodega = Bodega(resultado[1], resultado[2])
      bodega.id = resultado[0]
      bodegas.append(bodega)

    return bodegas

  @staticmethod
  def obtener_por_id(id):
    consulta = "SELECT * FROM bodegas WHERE id=%s"
    valores = (id,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    bodega = None
    if len(resultado) > 0:
      bodega = Bodega(resultado[0][1], resultado[0][2])
      bodega.id = resultado[0][0]
    return bodega

class Categoria:
  def __init__(self, nombre):
    self.conexion_db = ConexionBaseDatos()
    self.id = None
    self.nombre = nombre

  def guardar(self):
    consulta = "INSERT INTO categorias (nombre) VALUES (%s)"
    valores = (self.nombre,)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  def editar(self):
    consulta = "UPDATE categorias SET nombre=%s WHERE id=%s"
    valores = (self.nombre, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  @staticmethod
  def obtener_todos():
    consulta = "SELECT * FROM categorias"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    categorias = []
    for resultado in resultados:
      categoria = Categoria(resultado[1])
      categoria.id = resultado[0]
      categorias.append(categoria)

    return categorias
  
  @staticmethod
  def obtener_por_id(id):
    consulta = "SELECT * FROM categorias WHERE id=%s"
    valores = (id,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    categoria = None
    if len(resultado) > 0:
      categoria = Categoria(resultado[0][1])
      categoria.id = resultado[0][0]
    return categoria


class Usuario:
  def __init__(self, nombre_usuario, contrasena, tipo_usuario):
    self.conexion_db = ConexionBaseDatos()
    self.id = None
    self.nombre_usuario = nombre_usuario
    self.contrasena = contrasena
    self.tipo_usuario = tipo_usuario

  def guardar(self):
    consulta = "INSERT INTO usuarios (nombre_usuario, contrasena, tipo_usuario) VALUES (%s, %s, %s)"
    valores = (self.nombre_usuario, generate_password_hash(self.contrasena), self.tipo_usuario)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  def editar(self):
    if self.contrasena:
      consulta = "UPDATE usuarios SET nombre_usuario=%s, contrasena=%s, tipo_usuario=%s WHERE id=%s"
      valores = (self.nombre_usuario, generate_password_hash(self.contrasena), self.tipo_usuario, self.id)
    else:
      consulta = "UPDATE usuarios SET nombre_usuario=%s, tipo_usuario=%s WHERE id=%s"
      valores = (self.nombre_usuario, self.tipo_usuario, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  @staticmethod
  def obtener_todos():
    consulta = "SELECT * FROM usuarios"
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    usuarios = []
    for resultado in resultados:
      usuario = Usuario(resultado[1], resultado[2], resultado[3])
      usuario.id = resultado[0]
      usuarios.append(usuario)
    return usuarios

  @staticmethod
  def obtener_por_id(id):
    consulta = "SELECT * FROM usuarios WHERE id=%s"
    valores = (id,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    usuario = None
    if len(resultado) > 0:
      usuario = Usuario(resultado[0][1], resultado[0][2], resultado[0][3])
      usuario.id = resultado[0][0]
    return usuario

  @staticmethod
  def obtener_por_email(nombre_usuario):
    consulta = "SELECT * FROM usuarios WHERE nombre_usuario=%s"
    valores = (nombre_usuario,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    usuario = None
    if len(resultado) > 0:
      usuario = Usuario(resultado[0][1], resultado[0][2], resultado[0][3])
      usuario.id = resultado[0][0]
    return usuario

class Movimiento:
  def __init__(self, id_producto, id_bodega, cantidad, tipo_movimiento, usuario_id):
    self.conexion_db = ConexionBaseDatos()
    self.id = None
    self.id_producto = id_producto
    self.id_bodega = id_bodega
    self.cantidad = cantidad
    self.usuario_id = usuario_id
    self.tipo_movimiento = tipo_movimiento
    self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.fecha = datetime.strptime(self.fecha, '%Y-%m-%d %H:%M:%S')

  def guardar(self):
    consulta = "INSERT INTO movimientos (fecha, tipo_movimiento, cantidad, usuario_id, producto_id, bodega_id) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (self.fecha, self.tipo_movimiento, self.cantidad, self.usuario_id, self.id_producto, self.id_bodega)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  def editar(self):
    consulta = "UPDATE movimientos SET id_producto=%s, id_bodega=%s, cantidad=%s, usuario_id=%s tipo_movimiento=%s, fecha=%s WHERE id=%s"
    valores = (self.id_producto, self.id_bodega, self.cantidad, self.tipo_movimiento, self.fecha, self.id)
    self.conexion_db.ejecutar_consulta(consulta, valores)

  @staticmethod
  def obtener_todos():
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, productos.precio_compra, movimientos.usuario_id, usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE movimientos.usuario_id=usuarios.id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id
              """
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta)
    movimientos = []
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8] )
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos

  @staticmethod
  def obtener_todos_nombre_rango_fecha(nombre_producto, fecha_inicio, fecha_fin):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, productos.precio_compra, movimientos.usuario_id, usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE movimientos.usuario_id=usuarios.id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and productos.nombre_producto=%s and fecha BETWEEN %s AND %s
              """
    conexion_db = ConexionBaseDatos()
    valores = (nombre_producto, fecha_inicio+" 00:00:00", fecha_fin+" 23:59:59")
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8] )
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos


  @staticmethod
  def obtener_todos_rango_fecha(fecha_inicio, fecha_fin):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, productos.precio_compra, movimientos.usuario_id, usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE movimientos.usuario_id=usuarios.id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and fecha BETWEEN %s AND %s
              """
    conexion_db = ConexionBaseDatos()
    valores = (fecha_inicio+" 00:00:00", fecha_fin+" 23:59:59")
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8] )
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos
  @staticmethod
  def obtener_todos_nombre(nombre_producto):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, productos.precio_compra, movimientos.usuario_id, usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE movimientos.usuario_id=usuarios.id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and productos.nombre_producto=%s
              """
    conexion_db = ConexionBaseDatos()
    valores = (nombre_producto, )
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8] )
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos

  @staticmethod
  def obtener_por_id(id):
    consulta = "SELECT * FROM movimientos WHERE id=%s"
    valores = (id,)
    conexion_db = ConexionBaseDatos()
    resultado = conexion_db.ejecutar_consulta(consulta, valores)
    movimiento = None
    if len(resultado) > 0:
      movimiento = Movimiento(resultado[0][1], resultado[0][2], resultado[0][3], resultado[0][4])
      movimiento.id = resultado[0][0]
      movimiento.fecha = resultado[0][5]
    return movimiento

  @staticmethod
  def obtener_por_producto(producto_id):
    consulta = "SELECT * FROM movimientos WHERE id_producto=%s"
    valores = (producto_id,)
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4])
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5]
      movimientos.append(movimiento)
    return movimientos

  @staticmethod
  def obtener_por_bodega(bodega_id):
    consulta = "SELECT * FROM movimientos WHERE id_bodega=%s"
    valores = (bodega_id,)
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4])
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5]
      movimientos.append(movimiento)
    return movimientos
  
  @staticmethod
  def obtener_por_tipo_movimiento_rango_fecha(tipo, fecha_inicio, fecha_fin):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, precio_compra, movimientos.usuario_id, usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE usuarios.id= movimientos.usuario_id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and movimientos.tipo_movimiento=%s and fecha BETWEEN %s AND %s
              """
    valores = (tipo, fecha_inicio+" 00:00:00", fecha_fin+" 23:59:59")
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    # self.id_producto = id_producto
    # self.id_bodega = id_bodega
    # self.cantidad = cantidad
    # self.tipo_movimiento = tipo_movimiento
    # self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8])
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos
  
  @staticmethod
  def obtener_por_tipo_movimiento_rango_fecha_nombre_producto(tipo, fecha_inicio, fecha_fin, nombre_producto):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, precio_compra, movimientos.usuario_id, usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE usuarios.id= movimientos.usuario_id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and movimientos.tipo_movimiento=%s and productos.nombre_producto=%s and fecha BETWEEN %s AND %s
              """
    valores = (tipo, nombre_producto,fecha_inicio+" 00:00:00", fecha_fin+" 23:59:59")
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    # self.id_producto = id_producto
    # self.id_bodega = id_bodega
    # self.cantidad = cantidad
    # self.tipo_movimiento = tipo_movimiento
    # self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8])
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos


  @staticmethod
  def obtener_por_tipo_movimiento(tipo):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, productos.precio_compra, movimientos.usuario_id , usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE movimientos.usuario_id=usuarios.id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and movimientos.tipo_movimiento=%s
              """
    valores = (tipo,)
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    # self.id_producto = id_producto
    # self.id_bodega = id_bodega
    # self.cantidad = cantidad
    # self.tipo_movimiento = tipo_movimiento
    # self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8])
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos

  @staticmethod
  def obtener_por_tipo_movimiento_nombre_producto(tipo, nombre_producto):
    consulta = """SELECT movimientos.id, productos.nombre_producto, bodegas.nombre_bodega, movimientos.cantidad, movimientos.tipo_movimiento, movimientos.fecha, productos.precio_venta, productos.precio_compra, movimientos.usuario_id , usuarios.nombre_usuario
                  FROM movimientos, productos, bodegas, usuarios
                  WHERE movimientos.usuario_id=usuarios.id and movimientos.producto_id=productos.id and movimientos.bodega_id=bodegas.id and movimientos.tipo_movimiento=%s and productos.nombre_producto=%s
              """
    valores = (tipo, nombre_producto)
    conexion_db = ConexionBaseDatos()
    resultados = conexion_db.ejecutar_consulta(consulta, valores)
    movimientos = []
    # self.id_producto = id_producto
    # self.id_bodega = id_bodega
    # self.cantidad = cantidad
    # self.tipo_movimiento = tipo_movimiento
    # self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for resultado in resultados:
      movimiento = Movimiento(resultado[1], resultado[2], resultado[3], resultado[4], resultado[8])
      movimiento.id = resultado[0]
      movimiento.fecha = resultado[5].strftime("%Y-%m-%d %H:%M:%S")
      movimiento.precio_venta = resultado[6]
      movimiento.total_venta = (resultado[6]*resultado[3])
      movimiento.precio_compra = resultado[7]
      movimiento.total_compra = (resultado[7]*resultado[3])
      movimiento.usuario = resultado[9]
      movimientos.append(movimiento)
    return movimientos