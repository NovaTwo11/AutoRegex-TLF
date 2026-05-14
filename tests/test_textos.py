import sys
import os

# Ajustamos la ruta para que Python pueda encontrar nuestra carpeta 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.automata.escaner import EscanerTexto
from src.automata.validadores.validador_correo import ValidadorCorreo
from src.automata.validadores.validador_fecha import ValidadorFecha
from src.automata.validadores.validador_placa import ValidadorPlaca
from src.automata.validadores.validador_telefono import ValidadorTelefono
from src.automata.validadores.validador_url import ValidadorURL
from src.automata.validadores.validador_ip import ValidadorIP
from src.automata.validadores.validador_moneda import ValidadorMoneda
from src.automata.validadores.validador_documento import ValidadorDocumentoNIT

def ejecutar_prueba():
    print("🚀 Iniciando prueba del Escáner AutoRegex TLF...\n")

    # 1. Instanciamos nuestro "diccionario" de validadores
    mis_validadores = {
        "Correos": ValidadorCorreo(),
        "Fechas": ValidadorFecha(),
        "Placas": ValidadorPlaca(),
        "Teléfonos": ValidadorTelefono(),
        "URLs": ValidadorURL(),
        "IPs": ValidadorIP(),
        "Monedas": ValidadorMoneda(),
        "Documentos/NIT": ValidadorDocumentoNIT()
    }

    # 2. Inicializamos el escáner
    escaner = EscanerTexto(mis_validadores)

    # 3. Texto de prueba con varios patrones mezclados
    texto_prueba = """
    Hola, el día 15/08/2025 tenemos una reunión del proyecto. 
    Por favor confírmame al correo admin_123@empresa.com.co o revisa 
    los detalles en https://www.proyecto-tlf.com.
    El ingreso peatonal se hará con la cédula 1094123456, y para facturación 
    usaremos el NIT 900123456-1.
    El vehículo autorizado es el Mazda con placa XYZ789, y la moto escolta es ABC12D.
    Si hay fallas, llama al 3001234567. La conexión remota es a la IP 192.168.1.100.
    El presupuesto aprobado es de $1.500.000,00.
    """

    print("📄 Texto a analizar:")
    print("-" * 60)
    print(texto_prueba.strip())
    print("-" * 60, "\n")

    # 4. Extraemos los patrones
    resultados = escaner.extraer_patrones(texto_prueba)

    # 5. Mostramos los resultados limpios en consola
    print("🎯 Resultados de la extracción:")
    for categoria, coincidencias in resultados.items():
        if coincidencias:
            print(f"✅ {categoria}: {', '.join(coincidencias)}")
        else:
            print(f"❌ {categoria}: Ninguna coincidencia")

if __name__ == "__main__":
    ejecutar_prueba()