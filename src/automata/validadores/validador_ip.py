from ..motor_regex import AutomataBase


class ValidadorIP(AutomataBase):
    """
    Representa un Autómata Finito Extendido (EFSM) diseñado para validar direcciones IPv4
    en formato decimal separadas por puntos.

    Implementa memoria adicional para garantizar que cada uno de los cuatro octetos contenga
    un máximo de tres dígitos y represente un valor numérico en el rango válido de 0 a 255.

    Flujo de estados:
    - Estados 0, 4, 8, 12: Inician el procesamiento del primer, segundo, tercer y cuarto octeto, respectivamente. Requieren obligatoriamente un dígito numérico.
    - Estados 3, 7, 11: Procesan los dígitos subsiguientes de los primeros tres octetos y evalúan el separador '.' para transicionar al siguiente bloque.
    - Estado 15: Procesa los dígitos subsiguientes del cuarto octeto. Actúa como el único estado de aceptación de la cadena.
    - Estado -1: Estado sumidero. Representa una estructura inválida, longitud excesiva en un octeto o un valor fuera de rango.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[15])
        self.digitos_bloque = 0
        self.valor_bloque = 0

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados procesando los caracteres de entrada.
        Valida dinámicamente la longitud del octeto actual y calcula su valor numérico
        para garantizar que no exceda el límite del protocolo (255).
        """
        if self.estado_actual in [0, 4, 8, 12]:
            if caracter.isdigit():
                self.estado_actual += 3
                self.digitos_bloque = 1
                self.valor_bloque = int(caracter)
            else:
                self.estado_actual = -1

        elif self.estado_actual in [3, 7, 11, 15]:
            if caracter.isdigit():
                self.digitos_bloque += 1
                self.valor_bloque = (self.valor_bloque * 10) + int(caracter)

                if self.digitos_bloque > 3 or self.valor_bloque > 255:
                    self.estado_actual = -1

            elif caracter == '.' and self.estado_actual != 15:
                self.estado_actual += 1
                self.digitos_bloque = 0
                self.valor_bloque = 0
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1

    def validar(self, cadena):
        """
        Reinicia las variables de estado en memoria del autómata extendido e invoca
        el proceso de validación para una nueva cadena de entrada.
        """
        self.digitos_bloque = 0
        self.valor_bloque = 0
        return super().validar(cadena)