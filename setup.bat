@echo off
chcp 65001 >nul
echo ======================================
echo 🚀 Configurando entorno de desarrollo
echo ======================================

REM Verifica si ya existe la carpeta del entorno virtual
IF NOT EXIST env (
    echo 🔧 Creando entorno virtual...
    python -m venv env
)

REM Activa el entorno virtual
echo 🔌 Activando entorno virtual...
call env\Scripts\activate

REM Instala dependencias
echo 📦 Instalando dependencias desde requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Entorno configurado y listo.
echo ======================================
cmd /k