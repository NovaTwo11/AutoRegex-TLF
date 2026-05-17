from ..motor_regex import AutomataBase

class ValidadorCorreo(AutomataBase):
    """
    Autómata para validar estructura básica de correos.
    Estado 0: Obliga al menos un caracter alfanumérico al inicio.
    Estado 1: Leyendo el resto del usuario.
    Estado 2: Símbolo '@'.
    Estado 3: Primer caracter del dominio.
    Estado 4: Resto del dominio.
    Estado 5: Punto '.'.
    Estado 6: Extensión (Aceptación).
    """
    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[6])

    def transicion(self, caracter):
        if self.estado_actual == 0:
            # Exigimos al menos una letra o número antes de cualquier cosa
            if caracter.isalnum():
                self.estado_actual = 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 1:
            if caracter.isalnum() or caracter in ['.', '-', '_']:
                self.estado_actual = 1
            elif caracter == '@':
                self.estado_actual = 2
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            # El dominio debe empezar con letra o número
            if caracter.isalnum():
                self.estado_actual = 4
            else:
                self.estado_actual = -1

        elif self.estado_actual == 4:
            if caracter.isalnum() or caracter == '-':
                self.estado_actual = 4
            elif caracter == '.':
                self.estado_actual = 5
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            if caracter.isalpha():
                self.estado_actual = 6
            else:
                self.estado_actual = -1

        elif self.estado_actual == 6:
            if caracter.isalpha():
                self.estado_actual = 6
            elif caracter == '.':
                self.estado_actual = 5 # Permite dominios compuestos como .com.co
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1