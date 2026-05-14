from ..motor_regex import AutomataBase

class ValidadorDocumentoNIT(AutomataBase):
    """
    Autómata para Cédulas (6 a 10 dígitos) y NIT (9 dígitos + '-' + 1 dígito).
    Estados de aceptación:
    6, 7, 8, 9, 10 -> Cédulas válidas por longitud
    12 -> NIT válido
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[6, 7, 8, 9, 10, 12])

    def transicion(self, caracter):
        # Leemos los primeros 9 dígitos
        if 0 <= self.estado_actual < 9:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        # Al llegar al 9no dígito, se bifurca el camino
        elif self.estado_actual == 9:
            if caracter.isdigit():
                self.estado_actual = 10  # Cédula de 10 dígitos
            elif caracter == '-':
                self.estado_actual = 11  # Entrando a formato NIT
            else:
                self.estado_actual = -1

        elif self.estado_actual == 10:
            self.estado_actual = -1  # No se aceptan más de 10 dígitos para CC

        elif self.estado_actual == 11:
            if caracter.isdigit():
                self.estado_actual = 12  # Dígito de verificación del NIT
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1