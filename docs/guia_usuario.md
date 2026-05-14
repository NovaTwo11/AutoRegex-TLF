# Documentación Técnica y Guía de Usuario - AutoRegex TLF

## 1. Descripción de la Solución
AutoRegex TLF es una aplicación de escritorio desarrollada en Python orientada al reconocimiento y validación de patrones en textos, así como a la verificación de datos en interfaces interactivas[cite: 9]. La herramienta está dividida en dos módulos principales:
1. **Escáner de Textos:** Permite ingresar párrafos completos y extrae automáticamente información estructurada (correos, fechas, placas, etc.).
2. **Formularios Interactivos:** Una interfaz gráfica que valida en tiempo real la información ingresada por el usuario, otorgando retroalimentación visual inmediata sobre la validez de la cadena.

## 2. Explicación Técnica: Motor de Autómatas (Sin librerías predefinidas)
Para cumplir con los requerimientos del proyecto, **no se utilizaron librerías predefinidas de expresiones regulares (como `re` en Python)**. En su lugar, el procesamiento léxico y sintáctico [cite: 5] se construyó desde cero aplicando los fundamentos de los Autómatas Finitos (Teoría de Lenguajes Formales)[cite: 6, 10, 11].

### Arquitectura Lógica
* **Clase `AutomataBase`:** Funciona como la plantilla matemática. Define un `estado_inicial` (por defecto `0`) y una lista de `estados_aceptacion`. El método principal `validar(cadena)` recorre la entrada carácter por carácter, ejecutando la función de `transicion()`. Si en algún punto el autómata cae en un estado no definido (representado por `-1`), la cadena se rechaza inmediatamente[cite: 10].
* **Validadores Específicos:** Cada patrón (Correos, Placas, Fechas, etc.) [cite: 16, 17, 18, 19, 22] hereda de `AutomataBase` y sobrescribe el método de `transicion()`. 
    * *Ejemplo (Placas de Vehículos):* El autómata avanza del estado 0 al 2 si recibe letras[cite: 22]. Del estado 3 al 4 espera números. En el estado 5 se bifurca: si recibe un número, transita al estado 6 (Aceptación de Auto); si recibe una letra, transita al estado 7 (Aceptación de Moto).
* **Escáner (Analizador Léxico):** Para el procesamiento de textos largos, el sistema implementa una etapa de *tokenización*. Divide el texto por espacios, limpia signos de puntuación periféricos y evalúa cada "token" iterando sobre el diccionario de autómatas instanciados hasta encontrar un estado de aceptación[cite: 14, 15].

## 3. Guía Básica de Uso

### Instalación y Ejecución
1. Asegúrese de tener Python instalado en su sistema[cite: 50].
2. La interfaz gráfica requiere la librería estándar `tkinter` (incluida por defecto en la mayoría de las distribuciones de Python)[cite: 51].
3. Ejecute el archivo principal desde la terminal:
   ```bash
   python src/main.py