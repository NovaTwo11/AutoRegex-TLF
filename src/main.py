import tkinter as tk
import sys
import os

# Ajustamos la ruta para que Python reconozca la carpeta 'src' como un módulo válido.
# Esto evita el error "ModuleNotFoundError" al importar nuestros propios archivos.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos nuestra interfaz gráfica
from src.ui.app_window import AutoRegexApp


def main():
    print("🚀 Iniciando AutoRegex TLF...")

    # Creamos la raíz de la interfaz gráfica
    root = tk.Tk()

    # Instanciamos nuestra aplicación enviándole la raíz
    app = AutoRegexApp(root)

    # Iniciamos el bucle principal (mainloop) para que la ventana no se cierre
    root.mainloop()


if __name__ == "__main__":
    main()