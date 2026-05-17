from ..motor_regex import AutomataBase


class ValidadorFecha(AutomataBase):
    """
    Autómata Finito Extendido (EFSM) para validar fechas en formato DD/MM/AAAA, DD-MM-AAAA o DD.MM.AAAA.
    Asegura separadores consistentes y valida la existencia lógica de la fecha (meses, días y años bisiestos).
    """

    def __init__(self):
        super().__init__(estado_inicial=0, estados_aceptacion=[10])
        self.separador_usado = ''

        # Memoria del autómata extendido
        self.str_dia = ""
        self.str_mes = ""
        self.str_anio = ""

    def es_bisiesto(self, anio):
        """Regla matemática para determinar si un año es bisiesto."""
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    def validar_fecha_logica(self):
        """Valida que los días correspondan al mes y al año (bisiestos)."""
        dia = int(self.str_dia)
        mes = int(self.str_mes)
        anio = int(self.str_anio)

        # Límite básico de meses y días
        if mes < 1 or mes > 12: return False
        if dia < 1 or dia > 31: return False

        # Límite para años (Ajustado para el contexto de un Car Rental)
        if anio < 1900 or anio > 2100: return False

        # Validación de meses con 30 días
        meses_30 = [4, 6, 9, 11]
        if mes in meses_30 and dia > 30:
            return False

        # Validación específica para Febrero
        if mes == 2:
            if self.es_bisiesto(anio):
                if dia > 29: return False
            else:
                if dia > 28: return False

        return True

    def transicion(self, caracter):
        # Estados 0, 1: Leyendo el Día
        if self.estado_actual in [0, 1]:
            if caracter.isdigit():
                self.str_dia += caracter
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        # Estado 2: Primer separador
        elif self.estado_actual == 2:
            # Filtro temprano rápido
            if int(self.str_dia) == 0 or int(self.str_dia) > 31:
                self.estado_actual = -1
            elif caracter in ['/', '-', '.']:
                self.estado_actual = 3
                self.separador_usado = caracter
            else:
                self.estado_actual = -1

        # Estados 3, 4: Leyendo el Mes
        elif self.estado_actual in [3, 4]:
            if caracter.isdigit():
                self.str_mes += caracter
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        # Estado 5: Segundo separador (debe coincidir)
        elif self.estado_actual == 5:
            # Filtro temprano rápido
            if int(self.str_mes) == 0 or int(self.str_mes) > 12:
                self.estado_actual = -1
            elif caracter == self.separador_usado:
                self.estado_actual = 6
            else:
                self.estado_actual = -1

        # Estados 6, 7, 8: Leyendo los primeros 3 dígitos del año
        elif self.estado_actual in [6, 7, 8]:
            if caracter.isdigit():
                self.str_anio += caracter
                self.estado_actual += 1
            else:
                self.estado_actual = -1

        # Estado 9: Último dígito del año y transición a aceptación
        elif self.estado_actual == 9:
            if caracter.isdigit():
                self.str_anio += caracter

                # ¡Aquí ocurre la magia! Antes de aceptar, validamos la cronología
                if self.validar_fecha_logica():
                    self.estado_actual = 10
                else:
                    self.estado_actual = -1  # Se rechaza por ser fecha irreal
            else:
                self.estado_actual = -1
        else:
            self.estado_actual = -1

    def validar(self, cadena):
        # Sobrescribimos para limpiar toda la memoria antes de una nueva evaluación
        self.separador_usado = ''
        self.str_dia = ""
        self.str_mes = ""
        self.str_anio = ""
        return super().validar(cadena)