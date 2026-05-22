from ..motor_regex import AutomataBase


class ValidadorURL(AutomataBase):
    """
    Autómata para validar URLs con o sin protocolo (ej. www.nexo-uq.edu.co o https://...).
    Estados:
    0 a 7 -> Intentando validar protocolo 'http://' o 'https://'.
             Si el texto se desvía pero es válido, salta a leerlo como dominio.
    8 -> Leyendo dominio/subdominio
    9 -> Leyendo punto '.'
    10 -> Leyendo extensión (Estado de aceptación)
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[10])

    def transicion(self, caracter):
        # --- FASE 1: Análisis de Protocolo Opcional ---
        if self.estado_actual == 0:
            if caracter == 'h':
                self.estado_actual = 1
            elif caracter.isalnum():
                self.estado_actual = 8  # Si empieza por 'w', va directo al dominio
            else:
                self.estado_actual = -1

        elif self.estado_actual == 1:
            if caracter == 't':
                self.estado_actual = 2
            elif caracter == '.':
                self.estado_actual = 9
            elif caracter.isalnum() or caracter == '-':
                self.estado_actual = 8  # Ej: dominios como 'holdan.com'
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            if caracter == 't':
                self.estado_actual = 3
            elif caracter == '.':
                self.estado_actual = 9
            elif caracter.isalnum() or caracter == '-':
                self.estado_actual = 8
            else:
                self.estado_actual = -1

        elif self.estado_actual == 3:
            if caracter == 'p':
                self.estado_actual = 4
            elif caracter == '.':
                self.estado_actual = 9
            elif caracter.isalnum() or caracter == '-':
                self.estado_actual = 8
            else:
                self.estado_actual = -1

        elif self.estado_actual == 4:
            if caracter == 's':
                self.estado_actual = 5
            elif caracter == ':':
                self.estado_actual = 6
            elif caracter == '.':
                self.estado_actual = 9
            elif caracter.isalnum() or caracter == '-':
                self.estado_actual = 8
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            if caracter == ':':
                self.estado_actual = 6
            elif caracter == '.':
                self.estado_actual = 9
            elif caracter.isalnum() or caracter == '-':
                self.estado_actual = 8
            else:
                self.estado_actual = -1

        elif self.estado_actual == 6:  # Recibió los dos puntos ':'
            if caracter == '/':
                self.estado_actual = 7
            else:
                self.estado_actual = -1

        elif self.estado_actual == 7:  # Recibió la primera barra '/'
            if caracter == '/':
                self.estado_actual = 8  # Protocolo completo, inicia dominio
            else:
                self.estado_actual = -1

        # --- FASE 2: Lógica cíclica para dominios, subdominios y extensiones ---
        elif self.estado_actual == 8:
            if caracter.isalnum() or caracter == '-':
                self.estado_actual = 8
            elif caracter == '.':
                self.estado_actual = 9
            else:
                self.estado_actual = -1

        elif self.estado_actual == 9:
            # Recibió un punto, obligatoriamente sigue texto alfanumérico
            if caracter.isalnum():
                self.estado_actual = 10
            else:
                self.estado_actual = -1

        elif self.estado_actual == 10:
            # Estado de aceptación (ej. leyendo 'com' o 'co')
            # Ahora permitimos '/' para rutas y otros caracteres comunes en URLs
            if caracter.isalnum() or caracter in ['-', '_', '/', '?', '=', '&', '%']:
                self.estado_actual = 10
            elif caracter == '.':
                # Si hay otro punto (ej. com.co), vuelve al estado 9 para esperar más texto
                self.estado_actual = 9
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1