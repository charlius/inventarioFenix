from src.gestion_inventario_db import Usuario


usuario = Usuario("vendedor", "199314", "vendedor")
data = usuario.obtener_todos()
usuario.guardar()