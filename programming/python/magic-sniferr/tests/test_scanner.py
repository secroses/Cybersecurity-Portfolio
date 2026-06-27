"""
Tests unitarios y de integración para el módulo scanner.py (AutoFlow Hardened v0.1)
"""

import pytest
from pathlib import Path
from magic_sniffer.scanner import (
    sanitize_target_path,
    read_magic_bytes,
    inspect_file,
    scan_target
)


# =====================================================================
#  FIXTURES AUTOMÁTICAS (Generadores de archivos trampa en RAM)
# =====================================================================

@pytest.fixture
def valid_png_file(tmp_path):
    """Genera un archivo temporal PNG 100% válido."""
    file = tmp_path / "imagen_real.png"
    file.write_bytes(bytes.fromhex("89504e470d0a1a0a") + b"ContenidoFalsoPNG")
    return file


@pytest.fixture
def spoofed_file(tmp_path):
    """Genera un archivo trampa: Cabecera JPEG pero extensión .png"""
    file = tmp_path / "camuflado.png"
    file.write_bytes(bytes.fromhex("ffd8ffe000104a46") + b"ContenidoFalsoJPG")
    return file


@pytest.fixture
def nonexistent_file(tmp_path):
    """Devuelve una ruta que definitivamente no existe en el disco."""
    return tmp_path / "fantasma_404.exe"


# =====================================================================
#  SUITE DE PRUEBAS UNITARIAS POR COMPONENTE
# =====================================================================

class TestSanitizeTargetPath:
    """Tests de seguridad y saneamiento para sanitize_target_path()"""

    def test_valid_file_path(self, valid_png_file):
        result = sanitize_target_path(str(valid_png_file))
        assert result.exists()
        assert result.is_file()

    def test_nonexistent_file(self, nonexistent_file):
        with pytest.raises(FileNotFoundError):
            sanitize_target_path(str(nonexistent_file))

    def test_directory_path_raises_error(self, tmp_path):
        with pytest.raises(ValueError):
            sanitize_target_path(str(tmp_path))

    def test_zero_byte_file_protection(self, tmp_path):
        """[Hardening v0.1] Rechazar archivos de tamaño cero."""
        empty_file = tmp_path / "vacio.exe"
        empty_file.touch()
        with pytest.raises(ValueError, match="está vacío"):
            sanitize_target_path(str(empty_file))


class TestReadMagicBytes:
    """Tests de lectura binaria de bajo nivel para read_magic_bytes()"""

    def test_read_png_magic_bytes(self, valid_png_file):
        hex_bytes = read_magic_bytes(valid_png_file)
        assert hex_bytes.startswith("89504e47")

    def test_read_specific_byte_count(self, valid_png_file):
        hex_bytes = read_magic_bytes(valid_png_file, bytes_to_read=4)
        assert len(hex_bytes) == 8  # 4 bytes * 2 caracteres hex = 8

    def test_read_from_nonexistent_file(self, nonexistent_file):
        with pytest.raises(FileNotFoundError):
            read_magic_bytes(nonexistent_file)


class TestInspectFile:
    """Tests de evaluación de coherencia de identidad para inspect_file()"""

    def test_valid_png_file(self, valid_png_file):
        report = inspect_file(str(valid_png_file))
        assert report["real_type"] == "png"
        assert report["is_spoofed"] is False

    def test_spoofed_file(self, spoofed_file):
        report = inspect_file(str(spoofed_file))
        assert report["real_type"] == "jpg/jpeg"
        assert report["is_spoofed"] is True

    def test_unknown_magic_bytes(self, tmp_path):
        unknown = tmp_path / "misterio.dat"
        unknown.write_bytes(b"\xff\xfe\xfd\xfc" + b"\x00" * 20)
        report = inspect_file(str(unknown))
        assert report["real_type"] == "UNKNOWN"

    def test_report_structure(self, valid_png_file):
        report = inspect_file(str(valid_png_file))
        expected_keys = {
            "filename", "filepath", "declared_extension", "real_type",
            "mime_type", "description", "is_spoofed", "hex_header_sniffed"
        }
        assert expected_keys.issubset(report.keys())


class TestBatchScanner:
    """Tests de integración para la nueva función orquestadora scan_target()"""

    def test_scan_directory_batch(self, tmp_path, valid_png_file, spoofed_file):
        """Debe escanear una carpeta completa y devolver una lista de reportes."""
        # Colocamos ambos archivos dentro de la carpeta temporal tmp_path
        reports = scan_target(str(tmp_path))
        
        assert isinstance(reports, list)
        assert len(reports) == 2
        # Verificamos que capturó al culpable en el lote masivo
        assert any(r.get("is_spoofed") is True for r in reports)