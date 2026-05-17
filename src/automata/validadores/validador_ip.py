from ..motor_regex import AutomataBase


class ValidadorIP(AutomataBase):
    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[15])
        self.digitos_bloque = 0
        self.valor_bloque = 0  # Nueva variable para controlar el límite de 255

    def transicion(self, caracter):
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
                # Actualizamos el valor numérico del bloque
                self.valor_bloque = (self.valor_bloque * 10) + int(caracter)

                # Invalidamos si pasa de 3 dígitos o si el valor supera 255
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
        # Limpiamos la memoria antes de una nueva evaluación
        self.digitos_bloque = 0
        self.valor_bloque = 0
        return super().validar(cadena)