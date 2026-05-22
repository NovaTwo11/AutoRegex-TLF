from ..motor_regex import AutomataBase


class ValidadorPassword(AutomataBase):
    """
    Representa un Autómata Finito Extendido (EFSM) diseñado para validar el nivel
    de seguridad de contraseñas.

    Implementa memoria adicional mediante banderas lógicas para verificar el cumplimiento
    simultáneo de cuatro restricciones estructurales: longitud mínima de 8 caracteres,
    presencia de al menos una letra mayúscula, un dígito numérico y un carácter especial no alfanumérico.

    Flujo de estados:
    - Estado 0: Procesa la entrada y actualiza las métricas de evaluación. Actúa como estado de tránsito mientras la cadena no satisfaga todos los requerimientos de seguridad.
    - Estado 1: Estado de aceptación. Indica que la cadena procesada cumple integralmente con las políticas de complejidad y longitud establecidas.
    - Estado -1: Estado sumidero. Impide el procesamiento si el autómata ha entrado previamente en un estado inválido.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[1])
        self.tiene_mayus = False
        self.tiene_num = False
        self.tiene_esp = False
        self.longitud = 0

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados evaluando la tipología del carácter actual.
        Actualiza las variables de estado en memoria y transiciona al estado de aceptación
        únicamente cuando la secuencia global satisface todas las métricas de seguridad.
        """
        if self.estado_actual == -1:
            return

        self.longitud += 1

        if caracter.isupper():
            self.tiene_mayus = True
        elif caracter.isdigit():
            self.tiene_num = True
        elif not caracter.isalnum():
            self.tiene_esp = True

        if self.longitud >= 8 and self.tiene_mayus and self.tiene_num and self.tiene_esp:
            self.estado_actual = 1
        else:
            self.estado_actual = 0

    def validar(self, cadena):
        """
        Restablece las banderas lógicas y el contador de longitud en la memoria del
        autómata extendido antes de iniciar la evaluación de una nueva cadena.
        """
        self.tiene_mayus = False
        self.tiene_num = False
        self.tiene_esp = False
        self.longitud = 0
        return super().validar(cadena)