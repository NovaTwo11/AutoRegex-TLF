from ..motor_regex import AutomataBase

class ValidadorMoneda(AutomataBase):
    """
    Autómata para moneda. Inicia con $, seguido de números (puede tener . para miles y , para decimales).
    Estados de aceptación: 2 (entero) y 6 (con decimales)
    """
    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[2, 6])

    def transicion(self, caracter):
        if self.estado_actual == 0:
            if caracter == '$': self.estado_actual = 1
            else: self.estado_actual = -1
        elif self.estado_actual == 1:
            if caracter.isdigit(): self.estado_actual = 2
            else: self.estado_actual = -1
        elif self.estado_actual == 2:
            if caracter.isdigit(): self.estado_actual = 2
            elif caracter == '.': self.estado_actual = 3
            elif caracter == ',': self.estado_actual = 4
            else: self.estado_actual = -1
        elif self.estado_actual == 3: # Después de un punto de miles
            if caracter.isdigit(): self.estado_actual = 2
            else: self.estado_actual = -1
        elif self.estado_actual == 4: # Leyendo primer decimal
            if caracter.isdigit(): self.estado_actual = 5
            else: self.estado_actual = -1
        elif self.estado_actual == 5: # Leyendo segundo decimal
            if caracter.isdigit(): self.estado_actual = 6
            else: self.estado_actual = -1
        else:
            self.estado_actual = -1