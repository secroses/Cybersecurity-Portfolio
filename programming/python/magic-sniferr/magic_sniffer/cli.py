"""
Interfaz de línea de comandos para MagicSniffer.
Separada de main.py para mejor modularidad y testabilidad.
"""

import argparse
import json
import sys
from magic_sniffer.scanner import inspect_file


def create_parser():
    """Crea y retorna el parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog="magic-sniffer",
        description="MagicSniffer v0.1: Inspector determinista de file-spoofing.",
        epilog="Modo JSON output para automatización: magic-sniffer archivo.jpg --json",
    )
    parser.add_argument(
        "target",
        help="Ruta absoluta o relativa del archivo a analizar"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Devuelve el output en JSON crudo para automatizaciones"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose (más información de debug)"
    )
    return parser


def print_human_report(report):
    """Imprime un reporte legible para humanos."""
    print("\n" + "="*55)
    print(f" 🔍 INFORME DE TRIAGE BINARIO: {report.get('filename', 'ERROR')}")
    print("="*55)

    if "error" in report:
        print(f" ❌ FALLO DEL ESCÁNER: {report['error']}\n")
        return False

    print(f"  • Extensión declarada : .{report['declared_extension']}")
    print(f"  • Identidad Binaria   : {report['real_type'].upper()} ({report['description']})")
    print(f"  • Cabecera leída (Hex): {report['hex_header_sniffed']}...")

    if report["is_spoofed"]:
        print("\n [!] ⚠️ ALERTA DE SEGURIDAD: DESAJUSTE DE IDENTIDAD [!]")
        print("     El archivo intenta camuflarse. Su extensión no coincide con su cabecera.")
        print()
        return False
    else:
        print("\n [✓] Verificación superada: Identidad de archivo coherente.")
        print()
        return True


def main():
    """Función principal de la CLI."""
    parser = create_parser()
    args = parser.parse_args()

    report = inspect_file(args.target)

    # Modo JSON (Pipeline)
    if args.json:
        print(json.dumps(report, indent=2))
        if report.get("is_spoofed", False):
            sys.exit(2)
        sys.exit(0 if "error" not in report else 1)

    # Modo Humano (CLI)
    is_valid = print_human_report(report)
    
    if "error" in report:
        sys.exit(1)
    elif report.get("is_spoofed", False):
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
