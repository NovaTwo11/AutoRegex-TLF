# Documentación Técnica y Guía de Usuario - DriveTech

## 1. Descripción de la Solución
**AutoRegex TLF** es el panel de control administrativo de *DriveTech*, una Plataforma de Alquiler de Vehículos. La herramienta está orientada al reconocimiento y validación de patrones en textos, así como a la verificación de datos en interfaces interactivas. Se divide en tres módulos:
* **Nuevo Registro de Cliente:** Un formulario interactivo que valida en tiempo real datos críticos (correos, fechas, placas) antes de autorizar una reserva.
* **Auditoría de Contratos:** Un escáner de textos que permite importar documentos y extraer información estructurada de manera automática.
* **Laboratorio de Autómatas:** Una herramienta de Unit Testing visual para diagnosticar errores de formato en cadenas individuales.

## 2. Explicación Técnica: Motor de Autómatas

Para cumplir estrictamente con los requerimientos técnicos del proyecto, **la implementación se realizó sin recurrir a las librerías predefinidas de Python**. El procesamiento se construyó aplicando los fundamentos de los Autómatas Finitos y Autómatas Finitos Extendidos (EFSM).
### Arquitectura Lógica
* **Clase `AutomataBase`:** Plantilla matemática que define un `estado_inicial` y transita a través de una cadena de texto. Si cae en un estado no definido (representado por `-1`), la cadena se rechaza.
* **Autómatas Extendidos (EFSM):** Para patrones complejos como las *Fechas*, el autómata guarda variables temporales (`str_dia`, `str_mes`, `str_anio`) en cada estado para realizar cálculos cronológicos reales, como detectar años bisiestos.
* **Lógica de Negocio Basada en Estados:** El sistema utiliza el estado final de aceptación para tomar decisiones. Por ejemplo, en el validador de placas, el autómata termina en el **Estado 6** si es un Auto y en el **Estado 7** si es una Moto, permitiendo al formulario calcular la tarifa de alquiler dinámicamente.

## 3. Guía Básica de Uso
1. Asegúrese de tener **Python** instalado en su sistema.
2. La interfaz gráfica requiere la librería estándar `tkinter`, que viene incluida por defecto.
3. Ejecute el archivo principal desde la terminal de comandos:
   `python src/main.py`
4. Navegue por las pestañas superiores para registrar un cliente, escanear un contrato en texto plano (`.txt`) o utilizar el laboratorio de pruebas.