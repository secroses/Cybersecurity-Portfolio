"""
Configuración de pytest y fixtures compartidas.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_file():
    """Crea un archivo temporal para testing."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        yield Path(f.name)
    # Cleanup
    Path(f.name).unlink(missing_ok=True)


@pytest.fixture
def valid_png_file(temp_file):
    """Crea un archivo PNG válido para testing."""
    # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
    png_header = bytes.fromhex("89504e470d0a1a0a")
    with open(temp_file, "wb") as f:
        f.write(png_header)
        f.write(b"\x00" * 100)  # Contenido dummy
    return temp_file


@pytest.fixture
def spoofed_file(temp_file):
    """Crea un archivo disfrazado (JPG como PNG) para testing."""
    # JPEG magic bytes pero con extensión .png
    jpeg_header = bytes.fromhex("ffd8ffe0")
    with open(temp_file, "wb") as f:
        f.write(jpeg_header)
        f.write(b"\x00" * 100)
    return temp_file.with_suffix(".png")


@pytest.fixture
def nonexistent_file():
    """Retorna una ruta que no existe."""
    return Path("/tmp/nonexistent_file_12345.bin")
