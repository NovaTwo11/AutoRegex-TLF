class EscanerTexto:
    """
    Representa un analizador léxico diseñado para procesar secuencias de texto, extraer
    y clasificar patrones estructurales mediante la evaluación concurrente de múltiples
    autómatas finitos, operando sin dependencias de motores de expresiones regulares externos.
    """

    def __init__(self, diccionario_validadores):
        """
        Inicializa el analizador léxico inyectando un diccionario de instancias de autómatas validadores.
        """
        self.validadores = diccionario_validadores

    def limpiar_token(self, token):
        """
        Elimina los signos de puntuación situados en los extremos del token proporcionado
        para evitar interferencias estructurales durante la evaluación en los autómatas.
        """
        caracteres_puntuacion = '.,;:"\'()[]{}<>!?'
        return token.strip(caracteres_puntuacion)

    def extraer_patrones(self, texto):
        """
        Ejecuta el proceso de escaneo léxico sobre la cadena de entrada. Aplica tokenización
        por espacios, limpieza de caracteres periféricos y clasifica cada token válido iterando
        sobre el conjunto de autómatas registrados.

        Retorna un diccionario estructurado con las clasificaciones resultantes.
        """
        resultados = {clave: [] for clave in self.validadores.keys()}

        tokens = texto.split()

        for token in tokens:
            token_limpio = self.limpiar_token(token)

            if not token_limpio:
                continue

            for nombre_patron, automata in self.validadores.items():
                if automata.validar(token_limpio):
                    resultados[nombre_patron].append(token_limpio)
                    break

        return resultados