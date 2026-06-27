"""
Base de datos determinista de Magic Numbers.
Estructura: { "hex_signature": ("Extensiones_Reales", "Mime_Type", "Descripción") }

Esta base de datos está optimizada para detección de file-spoofing.
Las firmas están ordenadas de más específicas a más generales.
"""

MAGIC_DATABASE = {
    # Ejecutables - Windows
    "4d5a90": ("exe/dll", "application/x-msdownload", "Windows PE Executable (DOS MZ Header)"),
    "4d5a": ("exe/dll", "application/x-msdownload", "Windows PE Executable"),
    
    # Ejecutables - Unix/Linux
    "7f454c46": ("elf", "application/x-executable", "Linux ELF Executable"),
    "cafebabe": ("class/jar", "application/x-java-applet", "Java Class File"),
    
    # Documentos - PDF
    "25504446": ("pdf", "application/pdf", "PDF Document"),
    
    # Documentos - Microsoft Office Legacy (OLE2)
    "d0cf11e0a1b11ae1": ("doc/xls/ppt", "application/msword", "MS Office Legacy (OLE2)"),
    
    # Documentos - OpenXML (docx, xlsx, pptx son ZIP con estructura especial)
    "504b03040a0000": ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "Microsoft Word Document (DOCX)"),
    "504b030414000600": ("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "Microsoft Excel Spreadsheet (XLSX)"),
    "504b030414000600": ("pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "Microsoft PowerPoint Presentation (PPTX)"),
    
    # Archivos comprimidos - ZIP/JAR (genérico)
    "504b0304": ("zip/docx/xlsx/pptx/jar", "application/zip", "PKZIP Archive / OpenXML"),
    "504b0506": ("zip", "application/zip", "PKZIP Archive (empty)"),
    "504b0708": ("zip", "application/zip", "PKZIP Archive (span)"),
    
    # Archivos comprimidos - RAR
    "526172211a0700": ("rar", "application/x-rar-compressed", "RAR Archive v4"),
    "526172211a070100": ("rar", "application/x-rar-compressed", "RAR Archive v5"),
    
    # Archivos comprimidos - GZIP/TAR
    "1f8b08": ("gz/tar.gz", "application/gzip", "GZIP Archive"),
    "1f8b": ("gz", "application/gzip", "GZIP Archive (generic)"),

    # Archivos comprimidos - 7-Zip
    "377abcaf271c": ("7z", "application/x-7z-compressed", "7-Zip Archive"),

    # Imágenes - PNG
    "89504e470d0a1a0a": ("png", "image/png", "PNG Image"),
    
    # Imágenes - JPEG
    "ffd8ffe0": ("jpg/jpeg", "image/jpeg", "JPEG Image (JFIF)"),
    "ffd8ffe1": ("jpg/jpeg", "image/jpeg", "JPEG Image (EXIF)"),
    "ffd8ffe2": ("jpg/jpeg", "image/jpeg", "JPEG Image (ICC)"),
    "ffd8ffee": ("jpg/jpeg", "image/jpeg", "JPEG Image (Adobe)"),
    "ffd8ffdb": ("jpg/jpeg", "image/jpeg", "JPEG Image (DQT)"),
    "ffd8": ("jpg/jpeg", "image/jpeg", "JPEG Image (generic)"),
    
    # Imágenes - GIF
    "47494638": ("gif", "image/gif", "GIF Image (GIF8)"),
    
    # Imágenes - BMP
    "424d": ("bmp", "image/bmp", "BMP Image"),
    
    # Imágenes - TIFF
    "49492a00": ("tiff", "image/tiff", "TIFF Image (little-endian)"),
    "4d4d002a": ("tiff", "image/tiff", "TIFF Image (big-endian)"),
    
    # Imágenes - WebP
    "52494646": ("webp", "image/webp", "WebP Image (RIFF)"),
    
    # Imágenes - ICO
    "00000100": ("ico", "image/x-icon", "ICO Icon File"),
    
    # Audio - MP3
    "fffb": ("mp3", "audio/mpeg", "MP3 Audio (MPEG-1 Layer III)"),
    "fff3": ("mp3", "audio/mpeg", "MP3 Audio (MPEG-2 Layer III)"),
    "fffb90": ("mp3", "audio/mpeg", "MP3 Audio (MPEG-2.5 Layer III)"),
    "494433": ("mp3", "audio/mpeg", "MP3 Audio (ID3v2 Tag)"),
    
    # Audio - WAV
    "52494646": ("wav", "audio/wav", "WAV Audio (RIFF)"),
    
    # Audio - FLAC
    "664c6143": ("flac", "audio/flac", "FLAC Audio"),
    
    # Audio - OGG
    "4f676753": ("ogg", "audio/ogg", "OGG Vorbis/Opus"),
    
    # Video - MP4
    "00000020667479": ("mp4", "video/mp4", "MP4 Video"),
    "000000187469": ("mp4", "video/mp4", "MP4 Video (tiso)"),
    
    # Video - WebM
    "1a45dfa3": ("webm", "video/webm", "WebM Video"),
    
    # Video - Matroska (MKV)
    "1a45dfa3": ("mkv", "video/x-matroska", "Matroska Video (MKV)"),
    
    # Video - AVI
    "52494646": ("avi", "video/x-msvideo", "AVI Video (RIFF)"),
    
    # Texto - HTML (varios inicios posibles)
    "3c21444f43545950": ("html", "text/html", "HTML Document (DOCTYPE)"),
    "3c68746d6c": ("html", "text/html", "HTML Document (<html)"),
    "3c484541443e": ("html", "text/html", "HTML Document (<HEAD>)"),
    "0a3c": ("html", "text/html", "HTML Document (newline + <)"),
    
    # Texto - XML/XHTML
    "3c3f786d6c": ("xml", "application/xml", "XML Document"),
    
    # Texto - JSON (con BOM)
    "efbbbf7b": ("json", "application/json", "JSON Document (UTF-8 BOM)"),
    
    # Texto - Markdown (sin firma específica, se detecta por extensión)
    "232068": ("md", "text/markdown", "Markdown Document (# Header)"),
    
    # Ejecutables de Script - Bash
    "23212f62696e2f6261": ("sh", "text/x-shellscript", "Bash Script"),
    
    # Base de datos - SQLite
    "53514c69746520666f726d6174203320": ("db/sqlite", "application/x-sqlite3", "SQLite Database"),
    
    # Base de datos - MS Access
    "000100004a4f4552": ("mdb", "application/x-msaccess", "MS Access Database"),
}
