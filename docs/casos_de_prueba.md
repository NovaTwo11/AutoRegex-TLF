# Tabla de Casos de Prueba - DriveTech (AutoRegex TLF)

Este documento detalla la evaluación de la herramienta con textos y entradas variadas para comprobar su comportamiento. Se verifican tanto casos exitosos como fallidos para garantizar el manejo de errores controlados.

| Categoría / Autómata | Caso de Prueba (Entrada) | Resultado Esperado | Tipo de Caso | Justificación / Comportamiento del Autómata                                                                   |
| :--- | :--- | :--- | :--- |:--------------------------------------------------------------------------------------------------------------|
| **Placas (Vehículos)** | `XYZ789` | **Aceptado** | Exitoso | Cumple la estructura exacta de 3 letras seguidas de 3 números. El autómata termina en el estado 6 (Auto).     |
| **Placas (Motos)** | `ABC12D` | **Aceptado** | Exitoso | Cumple la estructura de 3 letras, 2 números y 1 letra final. El autómata termina en el estado 7 (Moto).       |
| **Placas** | `AB12` | **Rechazado** | Fallido | Faltan caracteres (tiene 4, deben ser 6). El autómata cae en estado de error.                                 |
| **Correos Electrónicos** | `admin_123@empresa.com.co` | **Aceptado** | Exitoso | Transita correctamente por usuario, `@`, dominio, `.` y extensiones.                                          |
| **Correos Electrónicos** | `sin_arroba.com` | **Rechazado** | Fallido | Nunca transita al estado 1 porque falta el carácter obligatorio `@`.                                          |
| **Fechas (Reserva)** | `29/02/2024` | **Aceptado** | Exitoso | Formato completo DD/MM/AAAA válido. El EFSM calcula lógicamente que 2024 es año bisiesto.                     |
| **Fechas (Reserva)** | `29/02/2023` | **Rechazado** | Fallido | El autómata extendido calcula la cronología y detecta que 2023 no fue bisiesto.                               |
| **Fechas (Reserva)** | `32/13/2023` | **Rechazado** | Fallido | Fecha irreal. Supera el límite matemático de días (31) y meses (12).                                          |
| **Teléfonos** | `3001234567` | **Aceptado** | Exitoso | La cadena contiene exactamente 10 dígitos numéricos.                                                          |
| **Teléfonos** | `300123456` | **Rechazado** | Fallido | Solo tiene 9 dígitos; no alcanza a llegar al estado de aceptación.                                            |
| **Direcciones IPv4** | `192.168.1.100` | **Aceptado** | Exitoso | Cuatro bloques de máximo 3 dígitos separados por puntos.                                                      |
| **Direcciones IPv4** | `300.168.1.100` | **Rechazado** | Fallido | El primer bloque excede el límite matemático de red de 255.                                                   |
| **Contraseñas Seguras**| `Admin123!` | **Aceptado** | Exitoso | El EFSM detecta longitud > 8, al menos 1 mayúscula, 1 número y 1 carácter especial.                           |
| **Contraseñas Seguras**| `admin123` | **Rechazado** | Fallido | Tiene la longitud correcta, pero las banderas de mayúscula y carácter especial son falsas.                    |
| **Documentos/NIT** | `900123456-1` | **Aceptado** | Exitoso | Formato NIT válido.                                                                                           |