from ..motor_regex import AutomataBase


class ValidadorPlaca(AutomataBase):
    """
    Representa un autómata finito determinista diseñado para validar el formato de placas
    vehiculares, diferenciando estructuralmente entre automóviles (tres letras seguidas de
    tres números) y motocicletas (tres letras, dos números y una letra final).

    Flujo de estados:
    - Estados 0, 1, 2: Procesan secuencialmente los tres caracteres alfabéticos iniciales obligatorios.
    - Estados 3, 4: Procesan secuencialmente los dos primeros dígitos numéricos obligatorios.
    - Estado 5: Evalúa el sexto carácter para determinar la tipología del vehículo y bifurcar el flujo.
    - Estado 6: Estado de aceptación. Indica un formato estructuralmente válido para un automóvil.
    - Estado 7: Estado de aceptación. Indica un formato estructuralmente válido para una motocicleta.
    - Estado -1: Estado sumidero. Representa una secuencia o formato de placa inválido.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[6, 7])

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados evaluando la posición y tipología (alfabética o numérica)
        de cada carácter para garantizar el cumplimiento de las normativas de formato vehicular.
        """
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
                self.estado_actual = 6
            elif caracter.isalpha():
                self.estado_actual = 7
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1