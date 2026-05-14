import tkinter as tk
from tkinter import ttk, messagebox

# Importamos nuestros validadores (Autómatas)
from src.automata.validadores.validador_correo import ValidadorCorreo
from src.automata.validadores.validador_password import ValidadorPassword
from src.automata.validadores.validador_telefono import ValidadorTelefono
from src.automata.validadores.validador_fecha import ValidadorFecha
from src.automata.validadores.validador_placa import ValidadorPlaca


class FormularioValidacion:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        self.motores = {
            "correo": ValidadorCorreo(),
            "password": ValidadorPassword(),
            "telefono": ValidadorTelefono(),
            "fecha": ValidadorFecha(),
            "placa": ValidadorPlaca()
        }

        # Nombres amigables para el cuadro de diálogo de errores
        self.nombres_campos = {
            "correo": "Correo Electrónico",
            "password": "Contraseña Segura",
            "telefono": "Teléfono Móvil",
            "fecha": "Fecha de Nacimiento",
            "placa": "Placa de Vehículo"
        }

        # Diccionario para rastrear el estado exacto de cada campo
        self.estado_campos = {k: {"valido": False, "mensaje": "El campo está vacío"} for k in self.motores.keys()}

        self.construir_campos()

    def construir_campos(self):
        self.parent.columnconfigure(1, weight=1)

        campos_info = [
            ("correo", "Correo Electrónico:", "ejemplo@dominio.com"),
            ("password", "Contraseña Segura:", "Mín 8 carácteres, 1 Mayús, 1 Núm, 1 Esp"),
            ("telefono", "Teléfono Móvil:", "10 dígitos"),
            ("fecha", "Fecha de Nacimiento:", "DD/MM/AAAA o DD-MM-AAAA"),
            ("placa", "Placa de Vehículo:", "Autos (ABC123) o Motos (ABC12D)")
        ]

        self.entradas = {}
        self.etiquetas_estado = {}

        for i, (identificador, texto_etiqueta, ayuda) in enumerate(campos_info):
            lbl = tk.Label(self.parent, text=texto_etiqueta, font=("Segoe UI", 10, "bold"),
                           bg="#ffffff", fg="#1f2937", anchor="e")
            lbl.grid(row=i, column=0, sticky="e", pady=15, padx=(0, 10))

            var_texto = tk.StringVar()
            var_texto.trace_add("write", lambda name, index, mode, id_campo=identificador,
                                                var=var_texto: self.validar_campo(id_campo, var))

            entry = tk.Entry(self.parent, textvariable=var_texto, font=("Segoe UI", 11),
                             bg="#f9fafb", relief="flat", highlightthickness=1,
                             highlightbackground="#d1d5db")
            entry.grid(row=i, column=1, sticky="we", pady=15, ipady=5)

            lbl_estado = tk.Label(self.parent, text=f"Formato: {ayuda}",
                                  font=("Segoe UI", 9, "italic"), bg="#ffffff",
                                  fg="#9ca3af", width=35, anchor="w")
            lbl_estado.grid(row=i, column=2, sticky="w", pady=15, padx=(10, 0))

            self.entradas[identificador] = entry
            self.etiquetas_estado[identificador] = lbl_estado

        self.btn_enviar = ttk.Button(self.parent, text="Validar y Enviar Datos",
                                     command=self.simular_envio)
        self.btn_enviar.grid(row=len(campos_info), column=1, sticky="e", pady=30)

    def obtener_recomendacion(self, identificador, texto):
        """Analiza la cadena para dar retroalimentación específica al usuario cuando el autómata la rechaza."""
        if identificador == "correo":
            if "@" not in texto: return "✗ Falta el símbolo '@'"
            if "." not in texto.split("@")[-1]: return "✗ Falta el dominio (ej. .com)"
            return "✗ Estructura de correo incompleta"

        elif identificador == "password":
            if len(texto) < 8: return f"✗ Faltan {8 - len(texto)} caracteres mínimos"
            if not any(c.isupper() for c in texto): return "✗ Falta al menos una letra mayúscula"
            if not any(c.isdigit() for c in texto): return "✗ Falta al menos un número"
            if not any(not c.isalnum() for c in texto): return "✗ Falta un carácter especial (ej. !@#$)"
            return "✗ Contraseña inválida"

        elif identificador == "telefono":
            if not texto.isdigit(): return "✗ Solo debe contener números"
            if len(texto) < 10: return f"✗ Faltan {10 - len(texto)} dígitos"
            if len(texto) > 10: return "✗ Sobran dígitos, deben ser 10 exactos"
            return "✗ Número inválido"

        elif identificador == "fecha":
            if len(texto) < 8: return "✗ Fecha muy corta o incompleta"
            return "✗ Formato inválido o separadores mixtos"

        elif identificador == "placa":
            if len(texto) < 6: return "✗ Faltan caracteres para la placa"
            return "✗ Estructura no coincide con Auto ni Moto"

        return "✗ Formato inválido"

    def validar_campo(self, identificador, var_texto):
        texto = var_texto.get()
        entry = self.entradas[identificador]
        lbl_estado = self.etiquetas_estado[identificador]

        if not texto:
            entry.config(highlightbackground="#d1d5db", highlightcolor="#4f46e5")
            lbl_estado.config(text="Campo vacío", fg="#9ca3af")
            self.estado_campos[identificador] = {"valido": False, "mensaje": "El campo está vacío"}
            return

        # El autómata determina la validez oficial
        es_valido = self.motores[identificador].validar(texto)

        if es_valido:
            entry.config(highlightbackground="#10b981", highlightcolor="#10b981")
            lbl_estado.config(text="✓ Formato válido", fg="#10b981", font=("Segoe UI", 9, "bold"))
            self.estado_campos[identificador] = {"valido": True, "mensaje": ""}
        else:
            entry.config(highlightbackground="#ef4444", highlightcolor="#ef4444")
            # Obtenemos la pista visual para el usuario
            recomendacion = self.obtener_recomendacion(identificador, texto)
            lbl_estado.config(text=recomendacion, fg="#ef4444", font=("Segoe UI", 9, "normal"))
            # Guardamos el mensaje (quitando la "✗ ") para el reporte final
            self.estado_campos[identificador] = {"valido": False, "mensaje": recomendacion.replace("✗ ", "")}

    def simular_envio(self):
        """Genera un reporte final consolidado de los errores."""
        errores_encontrados = []

        # Recorremos el diccionario de estados para armar la lista de errores
        for id_campo, estado in self.estado_campos.items():
            if not estado["valido"]:
                nombre = self.nombres_campos[id_campo]
                mensaje = estado["mensaje"]
                errores_encontrados.append(f"• {nombre}: {mensaje}")

        if len(errores_encontrados) == 0:
            messagebox.showinfo("Proceso Exitoso",
                                "Todos los datos cumplen con la estructura sintáctica y fueron aceptados por los autómatas.")
        else:
            # Unimos todos los errores con saltos de línea
            reporte_errores = "No se puede enviar el formulario. Corrige los siguientes puntos:\n\n" + "\n".join(
                errores_encontrados)
            messagebox.showwarning("Errores de Validación", reporte_errores)