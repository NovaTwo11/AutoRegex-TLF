from src.ui.formularios import FormularioValidacion

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importamos nuestro motor y validadores
from src.automata.escaner import EscanerTexto
from src.automata.validadores.validador_correo import ValidadorCorreo
from src.automata.validadores.validador_fecha import ValidadorFecha
from src.automata.validadores.validador_placa import ValidadorPlaca
from src.automata.validadores.validador_telefono import ValidadorTelefono
from src.automata.validadores.validador_url import ValidadorURL
from src.automata.validadores.validador_ip import ValidadorIP
from src.automata.validadores.validador_moneda import ValidadorMoneda
from src.automata.validadores.validador_documento import ValidadorDocumentoNIT


class AutoRegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoRegex TLF - Validador de Patrones")
        self.root.geometry("900x650")
        self.root.minsize(700, 550)
        self.root.configure(bg="#f4f5f7")

        # Inicializamos el motor de autómatas
        self.inicializar_motor()

        self.configurar_estilos()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=25, pady=25)

        self.tab_textos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_textos, text="   📄 Escáner de Textos   ")
        self.construir_tab_textos()

        self.tab_formularios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_formularios, text="   📝 Formulario Interactivo   ")
        self.construir_tab_formularios()

    def inicializar_motor(self):
        """Carga en memoria todos los autómatas sin usar librerías predefinidas."""
        mis_validadores = {
            "Correos Electrónicos": ValidadorCorreo(),
            "Fechas (DD/MM/AAAA)": ValidadorFecha(),
            "Placas (Autos/Motos)": ValidadorPlaca(),
            "Teléfonos": ValidadorTelefono(),
            "Direcciones URL": ValidadorURL(),
            "Direcciones IPv4": ValidadorIP(),
            "Valores Monetarios": ValidadorMoneda(),
            "Documentos y NIT": ValidadorDocumentoNIT()
        }
        self.escaner = EscanerTexto(mis_validadores)

    def configurar_estilos(self):
        # (El mismo código de estilos que ya teníamos)
        style = ttk.Style()
        style.theme_use('clam')
        bg_color = "#f4f5f7"
        card_bg = "#ffffff"
        accent_color = "#4f46e5"
        accent_hover = "#4338ca"
        text_color = "#1f2937"

        style.configure("TFrame", background=bg_color)
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[15, 8],
                        background="#e5e7eb", foreground=text_color, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", card_bg)], foreground=[("selected", accent_color)])
        style.configure("TLabelframe", background=card_bg, font=("Segoe UI", 11, "bold"),
                        foreground=text_color, borderwidth=1, bordercolor="#d1d5db", relief="solid")
        style.configure("TLabelframe.Label", background=card_bg, foreground=accent_color)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background=accent_color,
                        foreground="white", padding=10, borderwidth=0)
        style.map("TButton", background=[("active", accent_hover)])
        style.configure("TLabel", font=("Segoe UI", 11), background=bg_color, foreground=text_color)

    def construir_tab_textos(self):
        """Construye la interfaz para la búsqueda de patrones en textos y archivos."""
        frame_input = ttk.LabelFrame(self.tab_textos, text=" Texto a analizar ")
        frame_input.pack(fill='both', expand=True, padx=20, pady=(20, 10))

        # === NUEVO: Marco para agrupar los botones en la parte superior ===
        frame_botones_top = tk.Frame(frame_input, bg="#ffffff")
        frame_botones_top.pack(fill='x', padx=15, pady=(15, 0))

        self.btn_cargar = ttk.Button(frame_botones_top, text="📂 Cargar Archivo (.txt)",
                                     command=self.cargar_archivo)
        self.btn_cargar.pack(side='left')

        # Campo de texto
        self.txt_entrada = tk.Text(frame_input, height=8, wrap='word',
                                   font=("Segoe UI", 11), bg="#ffffff", fg="#1f2937",
                                   relief="flat", highlightthickness=1, highlightbackground="#d1d5db")
        self.txt_entrada.pack(fill='both', expand=True, padx=15, pady=(10, 15))

        # Botón de acción centrado
        self.btn_escanear = ttk.Button(self.tab_textos, text="🔍 Iniciar Escaneo de Patrones",
                                       command=self.procesar_texto)
        self.btn_escanear.pack(pady=5)

        frame_output = ttk.LabelFrame(self.tab_textos, text=" Resultados de la Extracción ")
        frame_output.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        self.txt_salida = tk.Text(frame_output, height=8, state='disabled',
                                  font=("Consolas", 11), bg="#f9fafb", fg="#374151",
                                  relief="flat", highlightthickness=1, highlightbackground="#e5e7eb")
        self.txt_salida.pack(fill='both', expand=True, padx=15, pady=15)

    def cargar_archivo(self):
        """Abre un cuadro de diálogo para seleccionar un archivo de texto y carga su contenido."""
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )

        if ruta_archivo:
            try:
                # Abrimos el archivo especificando la codificación UTF-8 para evitar problemas con tildes y ñ
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()

                # Limpiamos la caja de texto actual e insertamos el nuevo contenido
                self.txt_entrada.delete("1.0", tk.END)
                self.txt_entrada.insert(tk.END, contenido)

            except Exception as e:
                messagebox.showerror("Error de lectura", f"No se pudo leer el archivo.\nDetalle: {str(e)}")

    def procesar_texto(self):
        """Toma el texto de entrada, lo pasa por los autómatas y muestra el resultado."""
        # Obtenemos todo el texto desde la primera línea (1.0) hasta el final (tk.END)
        texto = self.txt_entrada.get("1.0", tk.END)

        # Ejecutamos nuestra lógica de análisis léxico
        resultados = self.escaner.extraer_patrones(texto)

        # Habilitamos la caja de salida para poder escribir en ella
        self.txt_salida.config(state='normal')
        self.txt_salida.delete("1.0", tk.END)  # Limpiamos resultados anteriores

        # Escribimos los nuevos resultados iterando el diccionario
        for categoria, coincidencias in resultados.items():
            if coincidencias:
                linea = f"✅ {categoria}: {', '.join(coincidencias)}\n"
            else:
                linea = f"❌ {categoria}: Ninguna coincidencia\n"

            self.txt_salida.insert(tk.END, linea)

        # Volvemos a deshabilitar la caja para que el usuario no pueda editar los resultados
        self.txt_salida.config(state='disabled')

    def construir_tab_formularios(self):
        frame_fondo = tk.Frame(self.tab_formularios, bg="#ffffff")
        frame_fondo.pack(fill='both', expand=True, padx=20, pady=20)

        lbl_info = tk.Label(frame_fondo, text="Validación de Entradas en Tiempo Real",
                            font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1f2937")
        lbl_info.pack(pady=(20, 5))

        lbl_sub = tk.Label(frame_fondo,
                           text="Ingresa los datos a continuación. El sistema verificará su estructura automáticamente.",
                           font=("Segoe UI", 10), bg="#ffffff", fg="#6b7280")
        lbl_sub.pack(pady=(0, 20))

        self.frame_campos = tk.Frame(frame_fondo, bg="#ffffff")
        self.frame_campos.pack(fill='both', expand=True, padx=40, pady=10)

        self.formulario = FormularioValidacion(self.frame_campos)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoRegexApp(root)
    root.mainloop()