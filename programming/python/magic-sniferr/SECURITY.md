# 🔐 SECURITY.md - MagicSniffer Security Guidelines

## Seguridad en Desarrollo

Este documento describe las mejores prácticas de seguridad para desarrollar y usar MagicSniffer.

---

## 🚨 ERRORES DE SEGURIDAD COMUNES (Evita estos)

### ❌ **Nunca commits estos archivos:**

```gitignore
# Datos sensibles
*.json (reportes locales)
*.xlsx (datos personales)
*.pdf (certificados, CVs con info personal)
*.docx (documentos privados)

# Información de identidad
*credentials*
*passwords*
*.pem
*.key
*.env.local

# Rutas de sistema local
reporte_*.json (contienen rutas absolutas C:\Users\...)
test_output/
local_config.py
```

### ✅ **Buena práctica antes de cada push:**

```bash
# 1. Revisar qué archivos vas a commitear
git status

# 2. Usar .gitignore ANTES de hacer commit
git add .gitignore
git commit -m "chore: update .gitignore"

# 3. Revisar cambios antes de push
git diff --cached

# 4. Solo entonces hacer push
git push origin main
```

---

## 📋 **Checklist de Seguridad Pre-Commit**

Antes de hacer `git push`, responde estas preguntas:

- [ ] ¿Contiene información personal (email, ruta de usuario)?
- [ ] ¿Hay rutas locales (C:\Users\..., /home/...)?
- [ ] ¿Incluye credenciales o tokens?
- [ ] ¿Son reportes de pruebas locales?
- [ ] ¿Hay archivos confidenciales (CVs, certificados)?

Si respondiste **SÍ** a cualquiera → **NO hagas push** → Agrega a `.gitignore` primero.

---

## 🛡️ **Validaciones de Seguridad en el Código**

MagicSniffer implementa:

### 1. **Límite de Tamaño de Archivo**
```python
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
# Previene análisis de archivos enormes que podrían consumir memoria
```

### 2. **Control de Recursión**
```python
MAX_RECURSION_DEPTH = 10
MAX_FILES_PER_SCAN = 10000
# Evita escaneos infinitos en directorios profundos
```

### 3. **Filtro de Rutas del Sistema**
```python
BLOCKED_PATHS = {'/sys', '/proc', '/dev', '/boot', '/root', 'Windows\\System32'}
# No analiza directorios críticos del SO
```

### 4. **Validación de Rutas**
```python
sanitize_target_path()  # Resuelve y valida antes de abrir archivos
```

---

## 🔒 **Configuración de Repositorio (GitHub)**

### Recomendaciones:

1. **Branch Protection Rules** (Main branch)
   - ✅ Requiere code review antes de merge
   - ✅ Requiere status checks (tests)
   - ✅ Descartar ramas obsoletas automáticamente

2. **Secret Scanning**
   - ✅ Activar "Push protection" en GitHub
   - ✅ Evita que se suban credenciales por error

3. **Dependabot**
   - ✅ Activar alertas de vulnerabilidades
   - ✅ Auto-actualizar dependencias peligrosas

---

## 📚 **Flujo de Trabajo Seguro (Workflow)**

```bash
# 1. Crear rama feature
git checkout -b feature/new-magic-detection
git push -u origin feature/new-magic-detection

# 2. Hacer cambios
# ... edita archivos ...

# 3. Review local ANTES de commit
git diff                    # Ve cambios
git status                  # Revisa archivos nuevos

# 4. Commit SOLO código
git add magic_sniffer/      # Solo carpeta del código
git commit -m "feat: add new magic signature"

# 5. Revisar ANTES de push
git log -1                  # Último commit
git diff origin/main        # Cambios respecto a main

# 6. Push y crear PR
git push origin feature/new-magic-detection
# ... crea PR en GitHub ...

# 7. GitHub Actions corre tests automáticamente
# No mergear si tests fallan
```

---

## 🚫 **Limpieza de Historial (Si Ya Cometiste Error)**

### Opción A: Eliminar archivo Y mantener en .gitignore
```bash
git rm --cached reporte_descargas.json
echo "reporte_*.json" >> .gitignore
git add .gitignore
git commit -m "SECURITY: Remove sensitive test files"
git push origin main
```

### Opción B: Limpiar completamente del historial (DESTRUCTIVO)
```bash
# Instalar BFG
brew install bfg  # macOS
# o descargar desde https://rtyley.github.io/bfg-repo-cleaner/

# Purgar archivo de TODO el historial
bfg --delete-files reporte_descargas.json .

# Limpiar referencias
git reflog expire --expire=now --all
git gc --prune=now

# Push con force (solo si eres el único contribuidor)
git push --force-with-lease origin main
```

---

## 🎓 **GitHub Student Developer Pack - MI RECOMENDACIÓN**

### ✅ **SÍ, SOLICÍTALO AHORA**

**Razones:**

1. **GitHub Copilot Pro** (gratis para estudiantes)
   - Autocomplete de código inteligente
   - Excelente para aprender

2. **GitHub Advanced Security**
   - Secret scanning (detecta credenciales)
   - Vulnerability alerts automáticos
   - Dependabot
   - Code scanning

3. **Otros beneficios**
   - JetBrains IDEs (PyCharm Professional)
   - DigitalOcean credits ($100/mes)
   - Namecheap domains (.me gratis)
   - Datadog monitoring
   - Heroku credits

### 📝 **Cómo Solicitarlo:**

1. Ve a https://education.github.com/pack
2. Click en "Get Student Benefits"
3. Verifica tu identidad (usa email universitario)
4. Selecciona tu escuela (si no aparece, puedes verificar manualmente)
5. GitHub enviará confirmación en días

### ⏰ **Timing (Importante):**

- **Tienes hasta 2029 antes de graduarte** ✅
- Aprovecha AHORA porque:
  - Acceso a herramientas profesionales GRATIS
  - Copilot + Advanced Security es oro puro para portfolio
  - Cuando te gradúes, pierdes beneficios (pero GitHub da 1 año extra)

---

## 🎯 **Resumen: Prevención de Futuros Errores**

| Acción | Cuándo | Por qué |
|--------|--------|---------|
| **Revisar `.gitignore`** | Antes de crear repo | Define qué NO sube |
| **`git status`** | Antes de cada commit | Ve exactamente qué subirás |
| **`git diff --cached`** | Antes de push | Revisa el contenido |
| **Usar rama feature** | Para cada cambio | No commiteas a main directamente |
| **GitHub Actions** | En cada push | Tests automáticos = validación |
| **Branch Protection** | Configurar repo | Requiere review antes de merge |
| **Secret Scanning** | Activar en Settings | GitHub alerta de credenciales |

---

## 📞 **¿Y si Cometo Error Nuevamente?**

1. **Detectas secreto en push** → `git push --force-with-lease` (local)
2. **Ya está en GitHub** → Opción B (BFG) + invalidar credenciales
3. **Dudas** → Revisa `.gitignore` primero

---

## 🔗 **Referencias Útiles**

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Git Best Practices](https://www.atlassian.com/git/tutorials/saving-changes)
- [Student Developer Pack](https://education.github.com/pack)

---

**Última actualización:** 2026-06-26  
**Autor:** MagicSniffer Security Team
