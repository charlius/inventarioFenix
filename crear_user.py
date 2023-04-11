from src.gestion_inventario_db import Usuario


usuario = Usuario("willson", "199312", "administrador")
data = usuario.obtener_todos()
usuario.guardar()