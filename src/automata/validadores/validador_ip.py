from ..motor_regex import AutomataBase

class ValidadorIP(AutomataBase):
    """
    Autómata para validar formato IPv4 básico (X.X.X.X donde X es 1 a 3 dígitos).
    """

    def __init__(self):
        # Los estados 3, 7, 11 y 15 representan el fin de la lectura de un bloque numérico válido.
        # Solo el 15 es aceptación porque representa el cuarto bloque.
        super().__init__(estado_inicial=0, estados_aceptacion=[15])
        self.digitos_bloque = 0

    def transicion(self, caracter):
        # Estados 0, 4, 8, 12: Inicio de un nuevo bloque
        if self.estado_actual in [0, 4, 8, 12]:
            if caracter.isdigit():
                self.estado_actual += 3  # Saltamos al estado de "leyendo bloque" (3, 7, 11, 15)
                self.digitos_bloque = 1
            else:
                self.estado_actual = -1

        # Estados 3, 7, 11, 15: Leyendo dígitos del bloque actual
        elif self.estado_actual in [3, 7, 11, 15]:
            if caracter.isdigit():
                self.digitos_bloque += 1
                if self.digitos_bloque > 3:
                    self.estado_actual = -1  # Error: más de 3 dígitos en un bloque
            elif caracter == '.' and self.estado_actual != 15:
                # Transición al siguiente bloque (4, 8, 12)
                self.estado_actual += 1
                self.digitos_bloque = 0
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1