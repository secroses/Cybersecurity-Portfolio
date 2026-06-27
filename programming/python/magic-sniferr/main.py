import argparse
import json
import sys
from magic_sniffer.scanner import scan_target

def main():
    parser = argparse.ArgumentParser(
        description="MagicSniffer v0.1: Inspector local determinista de file-spoofing."
    )
    parser.add_argument("target", help="Ruta absoluta o relativa del archivo o carpeta a analizar")
    parser.add_argument("--json", action="store_true", help="Devuelve el output en JSON crudo para automatizaciones")
    
    args = parser.parse_args()
    
    # scan_target ahora maneja tanto carpetas como archivos sueltos
    reports = scan_target(args.target)

    # Modo Pipeline (JSON masivo o individual)
    if args.json:
        print(json.dumps(reports, indent=2))
        # Si al menos un archivo está spoofed, salimos con código 2
        if any(r.get("is_spoofed", False) for r in reports):
            sys.exit(2)
        sys.exit(0 if not any("error" in r for r in reports) else 1)

    # Modo Humano (CLI)
    for report in reports:
        print("\n" + "="*55)
        print(f" 🔍 INFORME DE TRIAGE BINARIO: {report.get('filename', 'ERROR')}")
        print("="*55)

        if "error" in report:
            print(f" ❌ FALLO DEL ESCÁNER: {report['error']}\n")
            continue

        print(f"  • Ruta Física        : {report['filepath']}")
        print(f"  • Extensión declarada : .{report['declared_extension']}")
        print(f"  • Identidad Binaria   : {report['real_type'].upper()} ({report['description']})")
        print(f"  • Cabecera leída (Hex): {report['hex_header_sniffed']}...")

        if report["is_spoofed"]:
            print("\n [!] ⚠️ ALERTA DE SEGURIDAD: DESAJUSTE DE IDENTIDAD [!]")
            print("     El archivo intenta camuflarse. Su extensión no coincide con su cabecera.")
        else:
            print("\n [✓] Verificación superada: Identidad de archivo coherente.")
            
    # Verificar códigos de salida finales para el CLI
    if any(r.get("is_spoofed", False) for r in reports):
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()