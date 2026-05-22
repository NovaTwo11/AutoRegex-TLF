from ..motor_regex import AutomataBase


class ValidadorDocumentoNIT(AutomataBase):
    """
    Representa un autómata finito determinista diseñado para validar números de identificación,
    específicamente Cédulas de Ciudadanía (6 a 10 dígitos) y Números de Identificación Tributaria
    (NIT, estructurado como 9 dígitos, un guion y 1 dígito de verificación).

    Estados de aceptación:
    - Estados 6, 7, 8, 9, 10: Representan Cédulas válidas en función de su longitud.
    - Estado 12: Representa una estructura de NIT válida.
    - Estado -1: Estado sumidero. Representa una estructura inválida.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[6, 7, 8, 9, 10, 12])

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados del autómata evaluando dígitos numéricos y el guion separador del NIT.
        """
        if 0 <= self.estado_actual < 9:
            # Evalúa secuencialmente la entrada para acumular hasta los primeros 9 dígitos.
            if caracter.isdigit():
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 9:
            # Al alcanzar el noveno dígito, el autómata bifurca la validación entre
            # una Cédula máxima de 10 dígitos y el inicio del sufijo de un NIT.
            if caracter.isdigit():
                self.estado_actual = 10
            elif caracter == '-':
                self.estado_actual = 11
            else:
                self.estado_actual = -1

        elif self.estado_actual == 10:
            # Invalida secuencias numéricas continuas que superen los 10 dígitos permitidos para una Cédula.
            self.estado_actual = -1

        elif self.estado_actual == 11:
            # Evalúa el dígito de verificación para completar la estructura del NIT.
            if caracter.isdigit():
                self.estado_actual = 12
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1