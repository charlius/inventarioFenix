import mysql.connector

class ConexionBaseDatos:
  def __init__(self):
    self.conexion = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='',
      database='inventario'
    )
    self.cursor = self.conexion.cursor(buffered=True)

  def ejecutar_consulta(self, consulta, valores=None):
    self.cursor.execute(consulta, valores) if valores else self.cursor.execute(consulta)
    self.conexion.commit()
    print("paso")
    if "SELECT" in consulta:
      return self.cursor.fetchall()