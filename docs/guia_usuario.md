# Documentación Técnica y Guía de Usuario - DriveTech

## 1. Descripción de la Solución
[cite_start]**AutoRegex TLF** es el panel de control administrativo de *DriveTech*, una Plataforma de Alquiler de Vehículos[cite: 310]. [cite_start]La herramienta está orientada al reconocimiento y validación de patrones en textos, así como a la verificación de datos en interfaces interactivas[cite: 182]. Se divide en tres módulos:
* [cite_start]**Nuevo Registro de Cliente:** Un formulario interactivo que valida en tiempo real datos críticos (correos, fechas, placas) antes de autorizar una reserva[cite: 317].
* [cite_start]**Auditoría de Contratos:** Un escáner de textos que permite importar documentos y extraer información estructurada de manera automática[cite: 319, 320].
* [cite_start]**Laboratorio de Autómatas:** Una herramienta de Unit Testing visual para diagnosticar errores de formato en cadenas individuales[cite: 387].

## 2. Explicación Técnica: Motor de Autómatas
[cite_start]Para cumplir estrictamente con los requerimientos técnicos del proyecto, **la implementación se realizó sin recurrir a las librerías predefinidas de Python**[cite: 238, 239]. [cite_start]El procesamiento se construyó aplicando los fundamentos de los Autómatas Finitos y Autómatas Finitos Extendidos (EFSM)[cite: 304, 395].

### Arquitectura Lógica
* **Clase `AutomataBase`:** Plantilla matemática que define un `estado_inicial` y transita a través de una cadena de texto. Si cae en un estado no definido (representado por `-1`), la cadena se rechaza[cite: 304].
* [cite_start]**Autómatas Extendidos (EFSM):** Para patrones complejos como las *Fechas*, el autómata guarda variables temporales (`str_dia`, `str_mes`, `str_anio`) en cada estado para realizar cálculos cronológicos reales, como detectar años bisiestos[cite: 396, 398].
* **Lógica de Negocio Basada en Estados:** El sistema utiliza el estado final de aceptación para tomar decisiones. [cite_start]Por ejemplo, en el validador de placas, el autómata termina en el **Estado 6** si es un Auto y en el **Estado 7** si es una Moto, permitiendo al formulario calcular la tarifa de alquiler dinámicamente[cite: 367, 368, 381].

## 3. Guía Básica de Uso
1. [cite_start]Asegúrese de tener **Python** instalado en su sistema[cite: 223].
2. [cite_start]La interfaz gráfica requiere la librería estándar `tkinter`, que viene incluida por defecto[cite: 241].
3. Ejecute el archivo principal desde la terminal de comandos:
   `python src/main.py`
4. Navegue por las pestañas superiores para registrar un cliente, escanear un contrato en texto plano (`.txt`) o utilizar el laboratorio de pruebas.