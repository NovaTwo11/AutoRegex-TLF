import tkinter as tk
from tkinter import ttk, messagebox

# Importamos nuestros validadores (Autómatas)
from src.automata.validadores.validador_correo import ValidadorCorreo
from src.automata.validadores.validador_password import ValidadorPassword
from src.automata.validadores.validador_telefono import ValidadorTelefono
from src.automata.validadores.validador_fecha import ValidadorFecha
from src.automata.validadores.validador_placa import ValidadorPlaca


class FormularioRegistroCliente:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        self.motores = {
            "correo": ValidadorCorreo(),
            "password": ValidadorPassword(),
            "telefono": ValidadorTelefono(),
            "fecha": ValidadorFecha(),
            "placa": ValidadorPlaca()
        }

        # Nombres contextualizados al sistema de Car Rental
        self.nombres_campos = {
            "correo": "Correo de Notificaciones",
            "password": "Clave del Portal Cliente",
            "telefono": "Móvil de Contacto",
            "fecha": "Fecha de Inicio de Reserva",
            "placa": "Placa del Vehículo a Alquilar"
        }

        # Diccionario para rastrear el estado exacto de cada campo
        self.estado_campos = {k: {"valido": False, "mensaje": "Requerido para la reserva"} for k in self.motores.keys()}

        self.construir_campos()

    def construir_campos(self):
        # Marco central para alinear bien los elementos
        frame_grid = tk.Frame(self.parent, bg="white")
        frame_grid.pack(expand=True)

        campos_info = [
            ("correo", "Correo de Notificaciones:", "ejemplo@dominio.com"),
            ("password", "Clave del Portal Cliente:", "Mín 8 chars, 1 Mayús, 1 Núm, 1 Esp"),
            ("telefono", "Móvil de Contacto:", "10 dígitos exactos"),
            ("fecha", "Fecha de Inicio de Reserva:", "DD/MM/AAAA o DD-MM-AAAA"),
            ("placa", "Placa de Vehículo a Alquilar:", "Auto (ABC123) o Moto (ABC12D)")
        ]

        self.entradas = {}
        self.etiquetas_estado = {}

        for i, (id_campo, label_txt, ayuda) in enumerate(campos_info):
            # Etiquetas de los campos
            tk.Label(frame_grid, text=label_txt, font=("Segoe UI", 10, "bold"),
                     bg="white", fg="#334155", anchor="e").grid(row=i, column=0, sticky="e", pady=12, padx=(0, 15))

            var_texto = tk.StringVar()
            var_texto.trace_add("write", lambda n, i_x, m, id_c=id_campo, v=var_texto: self.validar_campo(id_c, v))

            # Entry más estético y corporativo
            entry = tk.Entry(frame_grid, textvariable=var_texto, font=("Segoe UI", 11),
                             bg="#f8fafc", width=30, relief="solid", borderwidth=1)
            entry.grid(row=i, column=1, sticky="w", pady=12, ipady=4)

            # Etiqueta de estado/ayuda
            lbl_estado = tk.Label(frame_grid, text=ayuda, font=("Segoe UI", 9),
                                  bg="white", fg="#94a3b8", width=35, anchor="w")
            lbl_estado.grid(row=i, column=2, sticky="w", pady=12, padx=(15, 0))

            self.entradas[id_campo] = entry
            self.etiquetas_estado[id_campo] = lbl_estado

        # Botón de acción principal
        btn_enviar = tk.Button(frame_grid, text="Autorizar Reserva de Vehículo",
                               font=("Segoe UI", 11, "bold"), bg="#10b981", fg="white",
                               activebackground="#059669", activeforeground="white",
                               relief="flat", padx=20, pady=8, command=self.simular_envio)
        btn_enviar.grid(row=len(campos_info), column=0, columnspan=3, pady=30)

    def obtener_recomendacion(self, id_campo, texto):
        """Analiza la cadena para dar retroalimentación específica al usuario cuando el autómata la rechaza."""
        if id_campo == "correo":
            if "@" not in texto: return "✗ Falta el símbolo '@'"
            if "." not in texto.split("@")[-1]: return "✗ Falta el dominio (ej. .com)"
            return "✗ Formato de correo corporativo inválido"

        elif id_campo == "password":
            if len(texto) < 8: return f"✗ Faltan {8 - len(texto)} caracteres mínimos"
            if not any(c.isupper() for c in texto): return "✗ Falta al menos una letra mayúscula"
            if not any(c.isdigit() for c in texto): return "✗ Falta al menos un número"
            if not any(not c.isalnum() for c in texto): return "✗ Falta un carácter especial (ej. !@#$)"
            return "✗ No cumple política de seguridad del portal"

        elif id_campo == "telefono":
            if not texto.isdigit(): return "✗ Solo debe contener números"
            if len(texto) < 10: return f"✗ Faltan {10 - len(texto)} dígitos"
            if len(texto) > 10: return "✗ Sobran dígitos, deben ser 10 exactos"
            return "✗ El móvil debe tener 10 dígitos sin espacios"

        elif id_campo == "fecha":
            if len(texto) < 8: return "✗ Fecha muy corta o incompleta"
            return "✗ Formato cronológico inválido"

        elif id_campo == "placa":
            if len(texto) < 6: return "✗ Faltan caracteres para la placa"
            return "✗ Placa no reconocida en el inventario (Auto/Moto)"

        return "✗ Formato inválido"

    def validar_campo(self, id_campo, var_texto):
        texto = var_texto.get()
        entry = self.entradas[id_campo]
        lbl_estado = self.etiquetas_estado[id_campo]

        if not texto:
            entry.config(highlightbackground="#d1d5db", highlightcolor="#2563eb")
            lbl_estado.config(text="Requerido para la reserva", fg="#94a3b8", font=("Segoe UI", 9, "normal"))
            self.estado_campos[id_campo] = {"valido": False, "mensaje": "Campo vacío"}
            return

        # El autómata determina la validez oficial
        es_valido = self.motores[id_campo].validar(texto)

        if es_valido:
            entry.config(highlightbackground="#10b981", highlightcolor="#10b981")

            # --- LÓGICA DE NEGOCIO BASADA EN ESTADOS DEL AUTÓMATA ---
            mensaje_exito = "✓ Dato verificado"

            if id_campo == "placa":
                estado_final = self.motores["placa"].estado_actual
                if estado_final == 6:
                    # El autómata se detuvo en estado de Aceptación 6 (Auto)
                    mensaje_exito = "✓ Vehículo: Auto - Tarifa: $150.000/día"
                elif estado_final == 7:
                    # El autómata se detuvo en estado de Aceptación 7 (Moto)
                    mensaje_exito = "✓ Vehículo: Moto - Tarifa: $60.000/día"

            lbl_estado.config(text=mensaje_exito, fg="#10b981", font=("Segoe UI", 9, "bold"))
            self.estado_campos[id_campo] = {"valido": True, "mensaje": ""}
        else:
            entry.config(highlightbackground="#ef4444", highlightcolor="#ef4444")
            # Obtenemos la pista visual para el usuario
            recomendacion = self.obtener_recomendacion(id_campo, texto)
            lbl_estado.config(text=recomendacion, fg="#ef4444", font=("Segoe UI", 9, "normal"))
            # Guardamos el mensaje (quitando la "✗ ") para el reporte final
            self.estado_campos[id_campo] = {"valido": False, "mensaje": recomendacion.replace("✗ ", "")}

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
            messagebox.showinfo("Reserva Aprobada",
                                "Todos los datos de contacto, facturación y placa vehicular han sido validados exitosamente en la plataforma.")
        else:
            # Unimos todos los errores con saltos de línea
            reporte_errores = "La plataforma ha rechazado el registro por las siguientes inconsistencias en la base de datos:\n\n" + "\n".join(
                errores_encontrados)
            messagebox.showwarning("Auditoría de Registro Fallida", reporte_errores)