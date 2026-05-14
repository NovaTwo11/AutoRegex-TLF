from ..motor_regex import AutomataBase

class ValidadorCorreo(AutomataBase):
    """
    Autómata para validar estructura básica de correos electrónicos.
    Estados:
    0 -> Nombre de usuario (alfanumérico, puntos, guiones)
    1 -> Símbolo '@'
    2 -> Dominio (alfanumérico)
    3 -> Punto '.'
    4 -> Extensión (letras). Estado de aceptación.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[4])

    def transicion(self, caracter):
        if self.estado_actual == 0:
            if caracter.isalnum() or caracter in ['.', '-', '_']:
                self.estado_actual = 0  # Nos mantenemos leyendo el usuario
            elif caracter == '@':
                self.estado_actual = 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 1:
            if caracter.isalnum():
                self.estado_actual = 2
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            if caracter.isalnum() or caracter == '-':
                self.estado_actual = 2  # Nos mantenemos leyendo el dominio
            elif caracter == '.':
                self.estado_actual = 3
            else:
                self.estado_actual = -1

        elif self.estado_actual == 3:
            if caracter.isalpha():
                self.estado_actual = 4
            else:
                self.estado_actual = -1

        elif self.estado_actual == 4:
            if caracter.isalpha():
                self.estado_actual = 4  # Seguimos leyendo la extensión
            elif caracter == '.':
                self.estado_actual = 3  # Caso de dominios como .com.co
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1