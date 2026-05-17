# AutoRegex TLF: DriveTech Rental Platform 🚗

[cite_start]Este proyecto fue desarrollado como parte de la asignatura de **Teoría de Lenguajes Formales**, con el objetivo de detectar y validar patrones en textos e interfaces interactivas[cite: 232]. 

[cite_start]Para demostrar el dominio técnico, **el motor de validación se construyó completamente desde cero utilizando el fundamento matemático de los Autómatas Finitos**, cumpliendo con la restricción estricta de no utilizar librerías predefinidas de expresiones regulares en Python[cite: 238, 239].

## Características Principales
El sistema se contextualizó como el panel de administración de una empresa de alquiler de vehículos (*DriveTech*), incorporando lógica de negocio basada en transiciones de estados:

* **Validación Lógica Rigurosa:** Autómatas Extendidos (EFSM) capaces de calcular límites de red (IPs) y años bisiestos (Fechas) sin depender de librerías externas.
* [cite_start]**Interfaz Interactiva (Tkinter):** Formularios que reaccionan en tiempo real, bloqueando el envío de inconsistencias a la base de datos[cite: 242, 243].
* **Lógica de Estados Aplicada:** El sistema determina automáticamente la tarifa de alquiler leyendo si el autómata finalizó en un estado de aceptación de Automóvil o de Motocicleta.
* **Escáner de Patrones:** Analizador léxico para extraer correos, URLs, monedas y teléfonos de contratos de alquiler en archivos `.txt`.

## Estructura del Proyecto
* `docs/`: Contiene la documentación, casos de prueba y guía de usuario.
* `src/automata/`: Contiene la clase `AutomataBase`, el escáner léxico y los validadores específicos.
* `src/ui/`: Contiene la interfaz gráfica y los formularios.
* `src/main.py`: Archivo principal para ejecutar la aplicación.

## Ejecución
```bash
python src/main.py