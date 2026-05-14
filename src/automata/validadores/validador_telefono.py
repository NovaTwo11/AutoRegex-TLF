from ..motor_regex import AutomataBase

class ValidadorTelefono(AutomataBase):
    """
    Autómata para validar números telefónicos de 10 dígitos.
    Estados:
    0 a 9 -> Leyendo dígitos
    10 -> Estado de aceptación (10 dígitos leídos)
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[10])

    def transicion(self, caracter):
        if 0 <= self.estado_actual < 10:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1  # Si hay más de 10 caracteres, se rechaza
