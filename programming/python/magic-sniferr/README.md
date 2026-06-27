# 🔍 MagicSniffer v0.1

**Inspector determinista de file-spoofing mediante análisis de magic numbers**

Un análisis de seguridad que detecta archivos que intentan camuflarse cambiando su extensión sin cambiar su contenido binario real.

## ⚡ ¿Qué es MagicSniffer?

MagicSniffer inspecciona la **cabecera binaria** (magic bytes/números mágicos) de un archivo y la compara con su extensión declarada. Si hay desajuste, significa que el archivo intenta **hacerse pasar por otro tipo**.

**Ejemplo de ataque:**
```bash
$ ls -la
-rw-r--r-- 1 user user 2.5M malware.jpg

$ file malware.jpg
malware.jpg: PE executable for MS Windows
```

## 🚀 Instalación

### Desde el repositorio
```bash
git clone https://github.com/secroses/cybersecurity-portfolio.git
cd cybersecurity-portfolio/programming/python/magic-sniffer/magic-sniffer
pip install -e .
```

### Requisitos
- Python 3.8+
- Sin dependencias externas (solo stdlib)

## 📖 Uso

### Modo CLI (Legible)
```bash
magic-sniffer /ruta/del/archivo.jpg
```

**Salida:**
```
=======================================================
 🔍 INFORME DE TRIAGE BINARIO: malware.jpg
=======================================================

  • Extensión declarada : .JPG
  • Identidad Binaria   : ELF (Linux ELF Executable)
  • Cabecera leída (Hex): 7f454c46...

 [!] ⚠️ ALERTA DE SEGURIDAD: DESAJUSTE DE IDENTIDAD [!]
     El archivo intenta camuflarse. Su extensión no coincide con su cabecera.
```

### Modo JSON (Pipeline)
```bash
magic-sniffer /ruta/del/archivo.jpg --json
```

**Salida:**
```json
{
  "filename": "malware.jpg",
  "declared_extension": "jpg",
  "real_type": "elf",
  "mime_type": "application/x-executable",
  "description": "Linux ELF Executable",
  "is_spoofed": true,
  "hex_header_sniffed": "7f454c46"
}
```

## 🔧 Códigos de Salida

| Código | Significado |
|--------|------------|
| 0 | ✅ Archivo legítimo (identidad coherente) |
| 1 | ❌ Error durante la ejecución |
| 2 | ⚠️ Archivo sospechoso (spoofing detectado) |

## 📁 Estructura del Proyecto

```
magic-sniffer/
├── magic_sniffer/
│   ├── __init__.py              # Inicializador del paquete
│   ├── cli.py                   # Interfaz de línea de comandos
│   ├── scanner.py               # Lógica de escaneo
│   └── database.py              # Base de datos de magic numbers
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py          # Tests unitarios
│   └── conftest.py              # Configuración de pytest
├── setup.py                     # Configuración de instalación
├── pyproject.toml               # Configuración moderna (PEP 517)
├── requirements.txt             # Dependencias
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=magic_sniffer

# Generar reporte HTML
pytest --cov=magic_sniffer --cov-report=html
```

## 🗄️ Magic Database

Los magic numbers soportados incluyen:

- **Ejecutables:** Windows PE (exe/dll), Linux ELF
- **Documentos:** PDF, MS Office Legacy (doc/xls/ppt)
- **Comprimidos:** ZIP, RAR, GZIP
- **Imágenes:** PNG, JPEG

Extensible en `magic_sniffer/database.py`

## 🛡️ Casos de Uso

- **Análisis forense:** Detectar malware disfrazado
- **Control de acceso:** Validar archivos subidos en formularios
- **Auditoría de seguridad:** Identificar anomalías en sistemas
- **Automatización DevSecOps:** Pipeline de CI/CD

## 📝 Licencia

Proyecto personal de demostración. No usar en producción sin auditoría.

## 👤 Autor

**secroses** - [GitHub](https://github.com/secroses)

---

*Hecho con ❤️ para la ciberseguridad*
