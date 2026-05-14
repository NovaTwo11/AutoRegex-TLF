from ..motor_regex import AutomataBase


class ValidadorFecha(AutomataBase):
    """
    Autómata Finito Extendido para validar fechas en formato DD/MM/AAAA, DD-MM-AAAA o DD.MM.AAAA.
    Asegura que el separador usado entre día y mes sea el mismo que entre mes y año.
    Estados:
    0, 1 -> Día (dígitos)
    2 -> Separador ('/', '-', '.')
    3, 4 -> Mes (dígitos)
    5 -> Separador (debe coincidir con el del estado 2)
    6, 7, 8 -> Año (primeros 3 dígitos)
    9 -> Año (último dígito y transición a aceptación)
    10 -> Estado de aceptación
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[10])
        self.separador_usado = ''

    def transicion(self, caracter):
        if self.estado_actual in [0, 1]:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            # Aceptamos barra, guion o punto, y lo guardamos en memoria
            if caracter in ['/', '-', '.']:
                self.estado_actual = 3
                self.separador_usado = caracter
            else:
                self.estado_actual = -1

        elif self.estado_actual in [3, 4]:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            # Exigimos estrictamente que el segundo separador sea igual al primero
            if caracter == self.separador_usado:
                self.estado_actual = 6
            else:
                self.estado_actual = -1

        elif self.estado_actual in [6, 7, 8]:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 9:
            if caracter.isdigit():
                self.estado_actual = 10
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1

    def validar(self, cadena):
        # Sobrescribimos para limpiar la memoria del separador antes de cada nueva evaluación
        self.separador_usado = ''
        return super().validar(cadena)