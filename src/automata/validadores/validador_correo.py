from ..motor_regex import AutomataBase


class ValidadorCorreo(AutomataBase):
    """
    Representa un autómata finito determinista diseñado para validar la estructura básica de direcciones de correo electrónico.

    Flujo de estados:
    - Estado 0: Evalúa el inicio de la cadena. Requiere un carácter alfanumérico.
    - Estado 1: Procesa el identificador del usuario. Admite alfanuméricos, puntos, guiones y guiones bajos.
    - Estado 2: Identifica el separador '@' e inicia la evaluación del dominio.
    - Estado 4: Procesa el cuerpo del dominio. Admite alfanuméricos y guiones.
    - Estado 5: Identifica el separador '.' que precede a la extensión.
    - Estado 6: Procesa la extensión del dominio (caracteres alfabéticos). Actúa como estado de aceptación y admite recursividad al Estado 5 para dominios compuestos.
    - Estado -1: Estado sumidero. Representa una estructura inválida.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[6])

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados del autómata basándose en el carácter de entrada actual.
        """
        if self.estado_actual == 0:
            # El identificador de usuario debe iniciar estrictamente con un carácter alfanumérico.
            if caracter.isalnum():
                self.estado_actual = 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 1:
            # Continúa la lectura del usuario o avanza al delimitador del dominio.
            if caracter.isalnum() or caracter in ['.', '-', '_']:
                self.estado_actual = 1
            elif caracter == '@':
                self.estado_actual = 2
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            # El nombre del dominio debe iniciar estrictamente con un carácter alfanumérico.
            if caracter.isalnum():
                self.estado_actual = 4
            else:
                self.estado_actual = -1

        elif self.estado_actual == 4:
            # Continúa la lectura del dominio o avanza al delimitador de extensión.
            if caracter.isalnum() or caracter == '-':
                self.estado_actual = 4
            elif caracter == '.':
                self.estado_actual = 5
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            # La extensión del dominio requiere exclusivamente caracteres alfabéticos.
            if caracter.isalpha():
                self.estado_actual = 6
            else:
                self.estado_actual = -1

        elif self.estado_actual == 6:
            # Procesa la extensión actual o retorna al estado 5 para procesar dominios de múltiples niveles.
            if caracter.isalpha():
                self.estado_actual = 6
            elif caracter == '.':
                self.estado_actual = 5
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1