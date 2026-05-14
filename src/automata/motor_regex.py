class AutomataBase:
    def __init__(self, estado_inicial=0, estados_aceptacion=None):
        self.estado_actual = estado_inicial
        self.estados_aceptacion = estados_aceptacion if estados_aceptacion else []

    def transicion(self, caracter):
        # Este método será sobrescrito por cada patrón específico
        # para definir cómo cambia de estado según el caracter ingresado.
        pass

    def validar(self, cadena):
        # Reiniciamos el estado al iniciar una validación
        self.estado_actual = 0

        # Procesamos cada caracter de la cadena de texto
        for caracter in cadena:
            self.transicion(caracter)

            # Si el autómata cae en un estado de error (ej. -1), se rechaza
            if self.estado_actual == -1:
                return False

        # Si al finalizar la cadena estamos en un estado válido, se acepta
        return self.estado_actual in self.estados_aceptacion