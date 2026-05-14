# Tabla de Casos de Prueba - AutoRegex TLF

[cite_start]Este documento detalla la evaluación de la herramienta con textos y entradas variadas, incluyendo ejemplos válidos e inválidos, con el fin de verificar el comportamiento esperado y el manejo de errores controlados por parte de los autómatas.

| Categoría / Autómata | Caso de Prueba (Entrada) | Resultado Esperado | Tipo de Caso | Justificación / Comportamiento del Autómata |
| :--- | :--- | :--- | :--- | :--- |
| **Placas (Vehículos)** | `XYZ789` | **Aceptado** | Exitoso | Cumple la estructura exacta de 3 letras seguidas de 3 números. |
| **Placas (Motos)** | `ABC12D` | **Aceptado** | Exitoso | Cumple la estructura de 3 letras, 2 números y 1 letra final. |
| **Placas** | `AB123` | **Rechazado** | Fallido | Longitud insuficiente; el autómata cae en estado de error (faltan letras o números). |
| **Placas** | `123ABC` | **Rechazado** | Fallido | El orden es incorrecto; el estado 0 espera una letra y recibe un dígito. |
| **Correos Electrónicos** | `admin_123@empresa.com.co` | **Aceptado** | Exitoso | Transita correctamente por usuario, `@`, dominio, `.` y extensiones. |
| **Correos Electrónicos** | `holdann.lopezs@uqvirtual.edu.co`| **Aceptado** | Exitoso | Valida correctamente múltiples puntos en el usuario y en la extensión del dominio. |
| **Correos Electrónicos** | `usuario@.com` | **Rechazado** | Fallido | Falla en el estado 1; después de `@` se espera texto alfanumérico para el dominio, no un `.`. |
| **Correos Electrónicos** | `sin_arroba.com` | **Rechazado** | Fallido | Nunca transita al estado 1 porque falta el carácter obligatorio `@`. |
| **Fechas** | `15/08/2025` | **Aceptado** | Exitoso | Formato completo DD/MM/AAAA válido. |
| **Fechas** | `1/8/25` | **Rechazado** | Fallido | No cumple con los dígitos obligatorios (el autómata espera 2 dígitos para día y mes). |
| **Fechas** | `15-08-2025` | **Rechazado** | Fallido | El separador esperado en los estados 2 y 5 es `/`, la entrada de `-` genera rechazo. |
| **Teléfonos** | `3001234567` | **Aceptado** | Exitoso | La cadena contiene exactamente 10 dígitos numéricos. |
| **Teléfonos** | `300123456` | **Rechazado** | Fallido | Solo tiene 9 dígitos; no alcanza a llegar al estado de aceptación 10. |
| **Teléfonos** | `30012345678` | **Rechazado** | Fallido | Excede los 10 dígitos; cualquier entrada en el estado 10 envía al autómata a rechazo. |
| **Direcciones URL** | `https://www.proyecto-tlf.com` | **Aceptado** | Exitoso | Valida el protocolo `https://`, el subdominio, el dominio y la extensión. |
| **Direcciones URL** | `htt://midominio.com` | **Rechazado** | Fallido | El protocolo está incompleto; no logra cruzar la validación estricta de caracteres iniciales. |
| **Direcciones IPv4** | `192.168.1.100` | **Aceptado** | Exitoso | Cuatro bloques de máximo 3 dígitos separados por puntos. |
| **Direcciones IPv4** | `192.168.1` | **Rechazado** | Fallido | Solo tiene 3 bloques; el autómata no alcanza el estado de aceptación final. |
| **Direcciones IPv4** | `192.168.1.1000` | **Rechazado** | Fallido | El cuarto bloque tiene 4 dígitos; el autómata detecta el exceso y envía a error. |
| **Monedas** | `$1.500.000,00` | **Aceptado** | Exitoso | Incluye el símbolo `$`, admite puntos de mil y coma decimal. |
| **Monedas** | `15000` | **Rechazado** | Fallido | No inicia con el símbolo obligatorio `$`. |
| **Documentos/NIT** | `1094123456` | **Aceptado** | Exitoso | Cédula válida de 10 dígitos. |
| **Documentos/NIT** | `900123456-1` | **Aceptado** | Exitoso | Formato NIT válido (9 dígitos, guion y dígito de verificación). |
| **Documentos/NIT** | `12345` | **Rechazado** | Fallido | Cédula inválida (solo 5 dígitos, no alcanza el estado mínimo de aceptación de 6). |
| **Contraseñas Seguras**| `Admin123!` | **Aceptado** | Exitoso | El EFSM detecta longitud > 8, al menos 1 mayúscula, 1 número y 1 carácter especial. |
| **Contraseñas Seguras**| `admin123` | **Rechazado** | Fallido | Tiene la longitud correcta, pero las banderas de mayúscula y carácter especial son falsas. |