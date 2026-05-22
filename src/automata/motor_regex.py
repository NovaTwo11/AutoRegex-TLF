class AutomataBase:
    """
    Representa la clase base para la implementación de autómatas finitos.
    Proporciona la estructura fundamental para la gestión de estados y el motor
    de procesamiento secuencial para la validación de cadenas de texto.
    """

    def __init__(self, estado_inicial=0, estados_aceptacion=None):
        """
        Inicializa la estructura base del autómata estableciendo el estado de partida
        y el conjunto de estados que determinan la validez de la cadena.
        """
        self.estado_actual = estado_inicial
        self.estados_aceptacion = estados_aceptacion if estados_aceptacion else []

    def transicion(self, caracter):
        """
        Define la interfaz abstracta para la lógica de transición de estados.
        Debe ser sobrescrita por las clases derivadas para definir el comportamiento
        específico del autómata frente a la evaluación de cada carácter de entrada.
        """
        pass

    def validar(self, cadena):
        """
        Ejecuta el procesamiento secuencial de la cadena de entrada.
        Restablece el estado inicial del autómata, evalúa cada carácter iterativamente
        mediante la función de transición e interrumpe el análisis si se alcanza un estado
        sumidero (-1). Retorna un valor booleano indicando si el flujo concluye en un
        estado de aceptación.
        """
        self.estado_actual = 0

        for caracter in cadena:
            self.transicion(caracter)

            if self.estado_actual == -1:
                return False

        return self.estado_actual in self.estados_aceptacion