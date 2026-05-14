class EscanerTexto:
    """
    Analizador léxico que recorre un texto para extraer los patrones
    usando los autómatas definidos, sin usar librerías de regex.
    """

    def __init__(self, diccionario_validadores):
        # Recibe un diccionario con las instancias de los validadores
        # Ej: {'Correos': ValidadorCorreo(), 'Fechas': ValidadorFecha()}
        self.validadores = diccionario_validadores

    def limpiar_token(self, token):
        """
        Elimina signos de puntuación al inicio y al final de la palabra
        para evitar que interfieran con la validación del autómata.
        """
        # Se pueden agregar más caracteres si es necesario
        caracteres_puntuacion = '.,;:"\'()[]{}<>!?'
        return token.strip(caracteres_puntuacion)

    def extraer_patrones(self, texto):
        """
        Escanea el texto y clasifica las coincidencias.
        Retorna un diccionario con los resultados.
        """
        # Inicializamos el diccionario de resultados
        resultados = {clave: [] for clave in self.validadores.keys()}

        # Tokenización: separamos el texto por espacios/saltos de línea
        tokens = texto.split()

        for token in tokens:
            token_limpio = self.limpiar_token(token)

            # Si el token quedó vacío tras la limpieza, lo saltamos
            if not token_limpio:
                continue

            # Evaluamos el token en cada autómata
            for nombre_patron, autómata in self.validadores.items():
                if autómata.validar(token_limpio):
                    # Si el autómata lo acepta, lo guardamos y rompemos el ciclo
                    # (asumiendo que un token no pertenece a dos categorías a la vez)
                    resultados[nombre_patron].append(token_limpio)
                    break

        return resultados