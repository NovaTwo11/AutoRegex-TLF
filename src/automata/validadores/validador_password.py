from ..motor_regex import AutomataBase

class ValidadorPassword(AutomataBase):
    """
    Autómata Finito Extendido (EFSM) para contraseñas.
    Reglas: Mínimo 8 caracteres, 1 mayúscula, 1 número, 1 caracter especial.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[1])
        self.tiene_mayus = False
        self.tiene_num = False
        self.tiene_esp = False
        self.longitud = 0

    def transicion(self, caracter):
        if self.estado_actual == -1:
            return

        self.longitud += 1

        if caracter.isupper():
            self.tiene_mayus = True
        elif caracter.isdigit():
            self.tiene_num = True
        elif not caracter.isalnum():
            self.tiene_esp = True

        # Si cumple con todos los requisitos, pasa al estado 1 (Aceptación)
        if self.longitud >= 8 and self.tiene_mayus and self.tiene_num and self.tiene_esp:
            self.estado_actual = 1
        else:
            self.estado_actual = 0  # Sigue leyendo, aún no es válida pero no hay error

    def validar(self, cadena):
        # Sobrescribimos el método validar para reiniciar las banderas en cada evaluación
        self.tiene_mayus = False
        self.tiene_num = False
        self.tiene_esp = False
        self.longitud = 0
        return super().validar(cadena)