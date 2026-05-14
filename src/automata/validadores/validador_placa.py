from ..motor_regex import AutomataBase

class ValidadorPlaca(AutomataBase):
    """
    Autómata para validar placas de Autos (3 letras, 3 números) y Motos (3 letras, 2 números, 1 letra).
    Estados:
    0 a 2 -> Esperando 3 letras iniciales
    3 a 4 -> Esperando 2 números
    5 -> Esperando el último caracter:
         - Si es número -> 6 (Aceptación Auto)
         - Si es letra -> 7 (Aceptación Moto)
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[6, 7])

    def transicion(self, caracter):
        if self.estado_actual in [0, 1, 2]:
            if caracter.isalpha():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual in [3, 4]:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            if caracter.isdigit():
                self.estado_actual = 6  # Es un Auto
            elif caracter.isalpha():
                self.estado_actual = 7  # Es una Moto
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1