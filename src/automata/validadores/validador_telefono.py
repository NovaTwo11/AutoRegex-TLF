from ..motor_regex import AutomataBase


class ValidadorTelefono(AutomataBase):
    """
    Representa un autómata finito determinista diseñado para validar números telefónicos
    con una longitud exacta de 10 dígitos.

    Flujo de estados:
    - Estados 0 a 9: Procesan secuencialmente cada uno de los dígitos numéricos requeridos.
    - Estado 10: Estado de aceptación. Indica que la cadena leída cumple con la estructura y longitud estipulada.
    - Estado -1: Estado sumidero. Representa un formato inválido, ya sea por la presencia de caracteres no numéricos o por exceder la longitud permitida.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[10])

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados evaluando secuencialmente la entrada para garantizar
        que esté compuesta exclusivamente por dígitos numéricos hasta alcanzar la longitud límite.
        """
        if 0 <= self.estado_actual < 10:
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1