from ..motor_regex import AutomataBase


class ValidadorFecha(AutomataBase):
    """
    Representa un Autómata Finito Extendido (EFSM) diseñado para validar cadenas con formato
    de fecha (DD/MM/AAAA, DD-MM-AAAA o DD.MM.AAAA).

    Implementa memoria para garantizar la consistencia en el uso de los separadores y valida
    la existencia cronológica de la fecha calculando límites de días según el mes y años bisiestos.

    Flujo de estados:
    - Estados 0, 1: Procesan los dígitos correspondientes al día.
    - Estado 2: Procesa el primer separador e inicializa la memoria del mismo.
    - Estados 3, 4: Procesan los dígitos correspondientes al mes.
    - Estado 5: Verifica que el segundo separador coincida exactamente con el primero.
    - Estados 6, 7, 8: Procesan los tres primeros dígitos del año.
    - Estado 9: Procesa el último dígito del año e invoca la validación lógica completa.
    - Estado 10: Estado de aceptación. Indica una fecha estructural y lógicamente válida.
    - Estado -1: Estado sumidero. Representa una estructura o fecha inválida.
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[10])
        self.separador_usado = ''

        self.str_dia = ""
        self.str_mes = ""
        self.str_anio = ""

    def es_bisiesto(self, anio):
        """
        Determina si el año proporcionado es bisiesto aplicando la validación matemática estándar.
        """
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    def validar_fecha_logica(self):
        """
        Verifica la validez cronológica de la fecha almacenada en memoria, evaluando los
        límites de meses, los días correspondientes a cada mes y la condición de año bisiesto.
        """
        dia = int(self.str_dia)
        mes = int(self.str_mes)
        anio = int(self.str_anio)

        if mes < 1 or mes > 12:
            return False
        if dia < 1 or dia > 31:
            return False

        if anio < 1900 or anio > 2100:
            return False

        meses_30 = [4, 6, 9, 11]
        if mes in meses_30 and dia > 30:
            return False

        if mes == 2:
            if self.es_bisiesto(anio):
                if dia > 29:
                    return False
            else:
                if dia > 28:
                    return False

        return True

    def transicion(self, caracter):
        """
        Ejecuta la transición de estados evaluando los caracteres para estructurar la fecha
        e invoca la validación lógica final al procesar el último dígito del año.
        """
        if self.estado_actual in [0, 1]:
            if caracter.isdigit():
                self.str_dia += caracter
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 2:
            if int(self.str_dia) == 0 or int(self.str_dia) > 31:
                self.estado_actual = -1
            elif caracter in ['/', '-', '.']:
                self.estado_actual = 3
                self.separador_usado = caracter
            else:
                self.estado_actual = -1

        elif self.estado_actual in [3, 4]:
            if caracter.isdigit():
                self.str_mes += caracter
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 5:
            if int(self.str_mes) == 0 or int(self.str_mes) > 12:
                self.estado_actual = -1
            elif caracter == self.separador_usado:
                self.estado_actual = 6
            else:
                self.estado_actual = -1

        elif self.estado_actual in [6, 7, 8]:
            if caracter.isdigit():
                self.str_anio += caracter
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        elif self.estado_actual == 9:
            if caracter.isdigit():
                self.str_anio += caracter

                if self.validar_fecha_logica():
                    self.estado_actual = 10
                else:
                    self.estado_actual = -1
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1

    def validar(self, cadena):
        """
        Reinicia la memoria extendida del autómata e inicia la validación de la cadena de entrada.
        """
        self.separador_usado = ''
        self.str_dia = ""
        self.str_mes = ""
        self.str_anio = ""
        return super().validar(cadena)