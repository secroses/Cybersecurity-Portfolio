import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from .database import MAGIC_DATABASE

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("MagicSniffer")

# Security hardening constants
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB limit
MAX_RECURSION_DEPTH = 10
MAX_FILES_PER_SCAN = 10000
BLOCKED_PATHS = {'/sys', '/proc', '/dev', '/boot', '/root', 'Windows\\System32'}


def sanitize_target_path(raw_path: str) -> Path:
    """Valida existencia, seguridad de IO y rechaza archivos de tamaño cero."""
    try:
        clean_path = Path(raw_path).resolve()
        
        if not clean_path.exists():
            raise FileNotFoundError(f"El objetivo no existe: {clean_path}")
            
        if clean_path.is_dir():
            return clean_path
            
        if not clean_path.is_file():
            raise ValueError(f"El objetivo no es un archivo regular: {clean_path}")
        
        # Check file size
        file_size = clean_path.stat().st_size
        if file_size == 0:
            raise ValueError(f"El archivo está vacío (0 bytes): {clean_path}")
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"El archivo excede límite de seguridad ({MAX_FILE_SIZE} bytes): {clean_path}")
            
        return clean_path
    except Exception as e:
        logger.error(f"Fallo en sanitización de ruta: {e}")
        raise


def is_system_path(path: Path) -> bool:
    """Verifica si la ruta es un directorio del sistema operativo (evitar análisis innecesarios)."""
    path_str = str(path).lower()
    return any(blocked in path_str for blocked in BLOCKED_PATHS)


def read_magic_bytes(file_path: Path, bytes_to_read: int = 16) -> str:
    """Lee estrictamente N bytes protegiendo la memoria del sistema."""
    try:
        with open(file_path, "rb") as target_file:
            raw_bytes = target_file.read(bytes_to_read)
            if not raw_bytes:
                raise ValueError(f"No se pudieron leer bytes del archivo: {file_path}")
            return raw_bytes.hex().lower()
    except (PermissionError, OSError) as e:
        logger.error(f"Error de acceso a bajo nivel en {file_path}: {e}")
        raise


def inspect_file(raw_path: str) -> Dict[str, Any]:
    """Inspecciona un archivo singular y determina su coherencia mágica."""
    try:
        target = sanitize_target_path(raw_path)
        
        # Si es directorio, error
        if target.is_dir():
            return {
                "filename": target.name,
                "error": "Se esperaba un archivo, se recibió un directorio. Usa scan_target() para directorios.",
                "is_spoofed": False
            }
        
        declared_ext = target.suffix.lower().replace(".", "")
        file_hex = read_magic_bytes(target, bytes_to_read=16)

        detected_info: Optional[tuple] = None
        sorted_signatures = sorted(MAGIC_DATABASE.keys(), key=len, reverse=True)

        for sig in sorted_signatures:
            if file_hex.startswith(sig):
                detected_info = MAGIC_DATABASE[sig]
                break

        report = {
            "filename": target.name,
            "filepath": str(target),
            "declared_extension": declared_ext if declared_ext else "NONE",
            "real_type": detected_info[0] if detected_info else "UNKNOWN",
            "mime_type": detected_info[1] if detected_info else "application/octet-stream",
            "description": detected_info[2] if detected_info else "Firma no catalogada",
            "is_spoofed": False,
            "hex_header_sniffed": file_hex[:16]
        }

        if detected_info and declared_ext:
            valid_extensions = detected_info[0].split("/")
            if declared_ext not in valid_extensions:
                report["is_spoofed"] = True

        return report

    except Exception as e:
        return {"filename": str(raw_path), "error": str(e), "is_spoofed": False}


def scan_target(raw_target: str, max_depth: int = MAX_RECURSION_DEPTH) -> List[Dict[str, Any]]:
    """
    Función Orquestadora: Capaz de discriminar entre un archivo suelto 
    o un directorio completo para escaneo recursivo (Batch Triage).
    
    Args:
        raw_target: Ruta del archivo o directorio
        max_depth: Profundidad máxima de recursión (default: 10)
    
    Returns:
        Lista de reportes de análisis
    """
    target_path = Path(raw_target).resolve()
    reports = []
    files_scanned = 0

    # Validar ruta inicial
    if not target_path.exists():
        return [{
            "filename": str(raw_target),
            "error": f"Ruta no existe: {raw_target}",
            "is_spoofed": False
        }]

    if is_system_path(target_path):
        logger.warning(f"Ruta de sistema detectada, saltando: {target_path}")
        return [{
            "filename": str(target_path),
            "error": f"Ruta protegida del sistema: {target_path}",
            "is_spoofed": False
        }]

    if target_path.is_file():
        return [inspect_file(str(target_path))]

    if target_path.is_dir():
        logger.info(f"Modo Directorio detectado. Escaneando: {target_path}")
        
        # Escaneamos de forma recursiva con limite de profundidad
        for file in target_path.rglob("*"):
            # Verificar limite de archivos
            if files_scanned >= MAX_FILES_PER_SCAN:
                logger.warning(f"Se alcanzó límite de {MAX_FILES_PER_SCAN} archivos")
                reports.append({
                    "filename": "SCAN_LIMIT",
                    "error": f"Se alcanzó límite de escaneo ({MAX_FILES_PER_SCAN} archivos)",
                    "is_spoofed": False
                })
                break
            
            # Verificar profundidad
            relative_parts = len(file.relative_to(target_path).parts)
            if relative_parts > max_depth:
                logger.debug(f"Profundidad máxima alcanzada, saltando: {file}")
                continue
            
            # Saltear rutas protegidas
            if is_system_path(file):
                logger.debug(f"Ruta protegida, saltando: {file}")
                continue
            
            if file.is_file():
                reports.append(inspect_file(str(file)))
                files_scanned += 1

    return reports
