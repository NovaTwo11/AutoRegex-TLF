import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.ui.formularios import FormularioRegistroCliente

from src.automata.escaner import EscanerTexto
from src.automata.validadores.validador_correo import ValidadorCorreo
from src.automata.validadores.validador_password import ValidadorPassword
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
        self.root.title("DriveTech - Plataforma de Alquiler de Vehículos")
        self.root.geometry("950x750")
        self.root.minsize(800, 650)
        self.bg_main = "#f0f2f5"
        self.root.configure(bg=self.bg_main)

        self.inicializar_motor()
        self.configurar_estilos()

        header = tk.Frame(self.root, bg="#1e293b", height=60)
        header.pack(fill='x', side='top')
        tk.Label(header, text="DRIVETECH RENTAL | Panel Administrativo",
                 font=("Segoe UI", 14, "bold"), bg="#1e293b", fg="white").pack(pady=15)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=30, pady=20)

        # Pestaña 1: Registro
        self.tab_registro = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_registro, text="  👤 Nuevo Registro de Cliente  ")
        self.construir_tab_registro()

        # Pestaña 2: Escáner
        self.tab_auditoria = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_auditoria, text="  📋 Auditoría de Contratos  ")
        self.construir_tab_auditoria()

        # Pestaña 3: Laboratorio de Pruebas
        self.tab_tester = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tester, text="  🧪 Laboratorio de Autómatas  ")
        self.construir_tab_tester()

    def inicializar_motor(self):
        # Mantenemos el diccionario para el escáner y el laboratorio
        self.validadores_instancias = {
            "Correo de Contacto": ValidadorCorreo(),
            "Contraseñas Seguras": ValidadorPassword(),
            "Fechas": ValidadorFecha(),
            "Placas de Vehículo": ValidadorPlaca(),
            "Teléfonos": ValidadorTelefono(),
            "URLs": ValidadorURL(),
            "Direcciones IP": ValidadorIP(),
            "Valores Monetarios": ValidadorMoneda(),
            "Identidad (CC/NIT)": ValidadorDocumentoNIT()
        }
        self.escaner = EscanerTexto(self.validadores_instancias)

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[20, 10],
                        background="#cbd5e1", foreground="#334155", borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", "#0f172a")])
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#2563eb", foreground="white", padding=8,
                        borderwidth=0)
        style.map("TButton", background=[("active", "#1d4ed8")])
        style.configure("TLabelframe", background="white", font=("Segoe UI", 11, "bold"), foreground="#1e293b",
                        borderwidth=1, bordercolor="#cbd5e1", relief="solid")
        style.configure("TLabelframe.Label", background="white", foreground="#2563eb")

    def construir_tab_registro(self):
        frame_fondo = tk.Frame(self.tab_registro, bg="white")
        frame_fondo.pack(fill='both', expand=True, padx=2, pady=2)
        tk.Label(frame_fondo, text="Alta de Cliente y Asignación de Vehículo", font=("Segoe UI", 16, "bold"),
                 bg="white", fg="#0f172a").pack(pady=(25, 5))
        tk.Label(frame_fondo,
                 text="El sistema validará estrictamente los datos para autorizar la reserva del vehículo.",
                 font=("Segoe UI", 10), bg="white", fg="#64748b").pack(pady=(0, 20))
        self.frame_campos = tk.Frame(frame_fondo, bg="white")
        self.frame_campos.pack(fill='both', expand=True, padx=40, pady=10)
        self.formulario = FormularioRegistroCliente(self.frame_campos)

    def construir_tab_auditoria(self):
        frame_input = ttk.LabelFrame(self.tab_auditoria, text=" Procesar Documento/Contrato ")
        frame_input.pack(fill='both', expand=True, padx=20, pady=(20, 10))
        frame_botones_top = tk.Frame(frame_input, bg="white")
        frame_botones_top.pack(fill='x', padx=15, pady=(15, 0))
        ttk.Button(frame_botones_top, text="📂 Importar Contrato (.txt)", command=self.cargar_archivo).pack(side='left')
        self.txt_entrada = tk.Text(frame_input, height=8, wrap='word', font=("Segoe UI", 10), bg="#f8fafc",
                                   fg="#1e293b", relief="solid", borderwidth=1, highlightthickness=0)
        self.txt_entrada.pack(fill='both', expand=True, padx=15, pady=(10, 15))
        ttk.Button(self.tab_auditoria, text="🔍 Extraer Datos Críticos del Documento", command=self.procesar_texto).pack(
            pady=5)
        frame_output = ttk.LabelFrame(self.tab_auditoria, text=" Reporte de Patrones Detectados ")
        frame_output.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        self.txt_salida = tk.Text(frame_output, height=8, state='disabled', font=("Consolas", 10), bg="#f1f5f9",
                                  fg="#334155", relief="solid", borderwidth=1, highlightthickness=0)
        self.txt_salida.pack(fill='both', expand=True, padx=15, pady=15)

    def construir_tab_tester(self):
        frame_fondo = tk.Frame(self.tab_tester, bg="white")
        frame_fondo.pack(fill='both', expand=True, padx=2, pady=2)

        tk.Label(frame_fondo, text="Modo Pruebas (Unit Testing Visual)", font=("Segoe UI", 16, "bold"), bg="white",
                 fg="#0f172a").pack(pady=(25, 5))
        tk.Label(frame_fondo,
                 text="Selecciona un autómata y prueba cadenas individuales. Recibirás un diagnóstico de fallos.",
                 font=("Segoe UI", 10), bg="white", fg="#64748b").pack(pady=(0, 20))

        frame_controles = tk.Frame(frame_fondo, bg="white")
        frame_controles.pack(pady=10)

        tk.Label(frame_controles, text="1. Selecciona el Autómata:", font=("Segoe UI", 10, "bold"), bg="white").grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
        self.combo_autómatas = ttk.Combobox(frame_controles, values=list(self.validadores_instancias.keys()),
                                            state="readonly", width=30, font=("Segoe UI", 10))
        self.combo_autómatas.current(0)
        self.combo_autómatas.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame_controles, text="2. Ingresa la cadena a evaluar:", font=("Segoe UI", 10, "bold"),
                 bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entrada_tester = tk.Entry(frame_controles, font=("Consolas", 12), width=32, bg="#f8fafc", relief="solid",
                                       borderwidth=1)
        self.entrada_tester.grid(row=1, column=1, padx=10, pady=10, ipady=4)

        ttk.Button(frame_controles, text="⚙️ Validar Cadena y Diagnosticar",
                   command=self.ejecutar_prueba_individual).grid(row=2, column=0, columnspan=2, pady=20)

        # La etiqueta de resultados ahora justificará el texto a la izquierda para las listas de errores
        self.lbl_resultado_tester = tk.Label(frame_fondo, text="Esperando entrada...", font=("Segoe UI", 12),
                                             bg="white", fg="#94a3b8", justify="left")
        self.lbl_resultado_tester.pack(pady=10)

    def obtener_diagnostico_error(self, nombre_validador, texto):
        """Genera un listado de los posibles motivos por los que el formato falló en el autómata."""
        errores = []
        if nombre_validador == "Correo de Contacto":
            if "@" not in texto: errores.append("Falta el símbolo '@'")
            if "." not in texto: errores.append("Falta un punto de dominio (ej. .com)")
            if texto.startswith("@") or texto.endswith("@"): errores.append("Estructura inválida alrededor del '@'")
            if not errores: errores.append("Caracteres no permitidos o no se detectó el dominio")

        elif nombre_validador == "Contraseñas Seguras":
            if len(texto) < 8: errores.append(f"Longitud insuficiente (faltan {8 - len(texto)} caracteres)")
            if not any(c.isupper() for c in texto): errores.append("Falta al menos una letra mayúscula")
            if not any(c.isdigit() for c in texto): errores.append("Falta al menos un número")
            if not any(not c.isalnum() for c in texto): errores.append("Falta un carácter especial (ej. !@#$)")

        elif nombre_validador == "Fechas":
            if len(texto) < 8: errores.append("Longitud insuficiente")
            if not ("/" in texto or "-" in texto or "." in texto): errores.append("Falta un separador válido (/, -, .)")
            if not errores: errores.append(
                "Los separadores están mezclados o la estructura de dígitos (DD/MM/AAAA) es inválida")

        elif nombre_validador == "Placas de Vehículo":
            if len(texto) < 6: errores.append(f"Faltan caracteres (Tiene {len(texto)}, deben ser 6)")
            if len(texto) > 6: errores.append("Sobran caracteres (Deben ser exactamente 6)")
            if len(texto) >= 3 and not texto[:3].isalpha(): errores.append(
                "Los primeros 3 caracteres deben ser letras obligatoriamente")
            if not errores: errores.append("Estructura no corresponde al Autómata de Auto (LLLNNN) o Moto (LLLNNL)")

        elif nombre_validador == "Teléfonos":
            if not texto.isdigit(): errores.append("Contiene caracteres no numéricos o espacios en blanco")
            if len(texto) < 10: errores.append(f"Faltan dígitos (Tiene {len(texto)}, deben ser 10)")
            if len(texto) > 10: errores.append(f"Excede los 10 dígitos obligatorios (Tiene {len(texto)})")

        elif nombre_validador == "URLs":
            if " " in texto: errores.append("La URL no debe contener espacios")
            if "." not in texto: errores.append("Falta el punto separador del dominio")
            if not errores: errores.append("El protocolo, el dominio principal o la extensión están malformados")

        elif nombre_validador == "Direcciones IP":
            bloques = texto.split(".")
            if len(bloques) != 4: errores.append(
                f"Debe tener exactamente 4 bloques separados por puntos (tiene {len(bloques)})")
            for b in bloques:
                if not b.isdigit():
                    errores.append(f"El bloque '{b}' contiene caracteres inválidos")
                elif int(b) > 255:
                    errores.append(f"El bloque '{b}' excede el límite matemático de red (255)")

        elif nombre_validador == "Valores Monetarios":
            if not texto.startswith("$"): errores.append("Debe iniciar obligatoriamente con el símbolo '$'")
            if not errores: errores.append("El formato de separadores de miles (.) o decimales (,) es incorrecto")

        elif nombre_validador == "Identidad (CC/NIT)":
            if len(texto) < 6: errores.append("La longitud es muy corta para ser Cédula o NIT")
            if "-" in texto and len(texto.split("-")[1]) != 1: errores.append(
                "El formato NIT exige exactamente 1 dígito de verificación tras el guión")
            if not errores: errores.append("No cumple el patrón de transición ni para Cédula (hasta 10 dígitos) ni NIT")

        return "\n".join([f"• {err}" for err in errores])

    def ejecutar_prueba_individual(self):
        nombre_validador = self.combo_autómatas.get()
        cadena = self.entrada_tester.get()

        if not cadena:
            self.lbl_resultado_tester.config(text="⚠️ Por favor ingresa una cadena en el campo de texto", fg="#f59e0b",
                                             font=("Segoe UI", 12, "bold"))
            return

        automata = self.validadores_instancias[nombre_validador]
        es_valido = automata.validar(cadena)

        if es_valido:
            self.lbl_resultado_tester.config(
                text=f"✅ ACEPTADO:\nLa cadena '{cadena}' pertenece al lenguaje formal y fue aceptada por el autómata.",
                fg="#10b981", font=("Segoe UI", 12, "bold")
            )
        else:
            # Ahora llamamos a nuestra nueva función de diagnóstico
            diagnostico = self.obtener_diagnostico_error(nombre_validador, cadena)
            mensaje_rechazo = f"❌ RECHAZADO:\nLa cadena '{cadena}' no es válida. Motivos probables detectados:\n\n{diagnostico}"
            self.lbl_resultado_tester.config(
                text=mensaje_rechazo,
                fg="#ef4444", font=("Segoe UI", 11, "normal")
            )

    def cargar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
        if ruta_archivo:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.txt_entrada.delete("1.0", tk.END)
                self.txt_entrada.insert(tk.END, archivo.read())

    def procesar_texto(self):
        texto = self.txt_entrada.get("1.0", tk.END)
        resultados = self.escaner.extraer_patrones(texto)
        self.txt_salida.config(state='normal')
        self.txt_salida.delete("1.0", tk.END)
        for categoria, coincidencias in resultados.items():
            if coincidencias:
                self.txt_salida.insert(tk.END, f"✅ {categoria}: {', '.join(coincidencias)}\n")
            else:
                self.txt_salida.insert(tk.END, f"❌ {categoria}: No detectado en el documento\n")
        self.txt_salida.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoRegexApp(root)
    root.mainloop()