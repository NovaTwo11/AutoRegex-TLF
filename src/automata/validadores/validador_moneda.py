from ..motor_regex import AutomataBase


class ValidadorMoneda(AutomataBase):
    """
    Representa un autómata finito determinista diseñado para validar formatos de moneda.
    Requiere el prefijo monetario ('$'), procesa la parte entera permitiendo puntos ('.')
    como separadores de miles y admite de forma opcional una coma (',') seguida exactamente
    de dos posiciones decimales.

    Flujo de estados:
    - Estado 0: Evalúa el inicio de la cadena. Requiere el carácter '$'.
    - Estado 1: Inicia el procesamiento de la magnitud numérica. Requiere un dígito.
    - Estado 2: Procesa la parte entera. Actúa como estado de aceptación para valores sin decimales. Habilita la transición a separadores de miles o al separador decimal.
    - Estado 3: Gestiona la secuencia posterior al separador de miles y retorna al flujo de la parte entera.
    - Estado 4: Procesa el primer dígito tras el separador decimal.
    - Estado 5: Procesa el segundo dígito decimal.
    - Estado 6: Estado de aceptación. Indica un formato monetario válido con extensión decimal exacta.
    - Estado -1: Estado sumidero. Representa un formato monetario inválido.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[2, 6])

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados evaluando posicionalmente el símbolo monetario,
        la secuencia de dígitos y el uso normativo de los separadores numéricos.
        """
        if self.estado_actual == 0:
            if caracter == '$':
                self.estado_actual = 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 1:
            if caracter.isdigit():
                self.estado_actual = 2
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            if caracter.isdigit():
                self.estado_actual = 2
            elif caracter == '.':
                self.estado_actual = 3
            elif caracter == ',':
                self.estado_actual = 4
            else:
                self.estado_actual = -1

        elif self.estado_actual == 3:
            if caracter.isdigit():
                self.estado_actual = 2
            else:
                self.estado_actual = -1

        elif self.estado_actual == 4:
            if caracter.isdigit():
                self.estado_actual = 5
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            if caracter.isdigit():
                self.estado_actual = 6
            else:
                self.estado_actual = -1

        else:
            self.estado_actual = -1