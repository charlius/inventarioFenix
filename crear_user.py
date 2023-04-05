from src.gestion_inventario_db import Usuario


usuario = Usuario("charles", "199314", "administrador")
data = usuario.obtener_todos()
usuario.guardar()