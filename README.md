# SIGEU - Sistema de Gestión de Eventos Universitarios

[![Python](https://img.shields.io/badge/python-3.13.7-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.6-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-internal-orange)]()

---

## 📌 Descripción

SIGEU es un **sistema web** desarrollado en Django para la gestión integral de **eventos universitarios**, incluyendo:

- Registro y autenticación de usuarios.
- Gestión de organizaciones externas.
- Registro, seguimiento y control de eventos.
- Control de acceso por roles: administrador, docente, estudiante, secretaria académica.
- Notificaciones y alertas automáticas.
- Cumplimiento de buenas prácticas de desarrollo y separación de responsabilidades.

---

## 🛠 Tecnologías

- Python 3.13.7
- Django 5.2.6
- MySQL / MariaDB
- HTML5, CSS3, JavaScript
- Librerías JS: SweetAlert2, Notyf
- Python-dotenv

---

## ⚙ Requisitos

- Python 3.13.7
- XAMPP / MySQL instalado
- Git
- Navegador moderno (Chrome, Firefox, Edge)

---

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/sigeu.git
cd sigeu
```

2. Ejecutar el entorno virtual:
```bash
setup.bat
```
Esto creará `env/`, instalará dependencias y activará el entorno virtual.

3. Configurar variables de entorno:
- Copiar `.env.template` como `.env`.
- Agregar la contraseña de la base de datos y otros valores sensibles.

4. Crear la base de datos y usuario:
- Nombre: definido en `.env` (ej: `sigeu`)
- Usuario: `django-user`
- Conceder todos los permisos

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Iniciar servidor:
```bash
python manage.py runserver
```

---

## 📁 Estructura del Proyecto

```
sigeu/
│
├── manage.py
├── sigeu/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── layouts/
│   │   ├── base.html
│   │   └── dashboard.html
│   └── components/
├── static/
│   ├── assets/
│   │   ├── img/
│   │   ├── icons/
│   │   └── favicon/
│   ├── css/
│   │   ├── base.css
│   │   └── components/
│   └── js/
│       ├── main.js
│       └── modules/
├── apps/
│   └── nombre_app/
│       ├── admin.py
│       ├── models.py
│       ├── urls.py
│       ├── services/
│       │   └── <archivo por modelo>.py
│       ├── views/
│       │   └── <archivo por grupo de funciones>.py  # cuando aplique
│       ├── forms/
│       │   └── <archivo por formulario>.py
│       ├── templates/
│       │   └── nombre_app/
│       │       ├── layouts/
│       │       └── components/
│       └── static/
│           └── nombre_app/
│               ├── assets/
│               ├── css/
│               └── js/
├── .gitignore
├── .env
└── .env.template
```

---

## 🌿 Flujo de Trabajo con Git

- Ramas principales:
  - `main`: Producción
  - `develop`: Desarrollo
- Ramas por funcionalidad:
  - Formato: `nombre-historia-usuario`
  - Ejemplo: `registro-usuario`, `autenticacion-usuarios`, `registro-organizacion-externa`
- Pull requests siempre hacia `develop`.
- Revisión y aprobación por el líder del proyecto.

### Convenciones de commits

- Estructura: `EMOJI acción: Verbo en infinitivo + descripción` (en inglés)
- Emojis: [Gitmoji](https://gitmoji.dev/)
- Acciones frecuentes:
  - `feat` → Nueva funcionalidad
    - Ejemplo: `✨ feat: add user registration`
  - `fix` → Corrección de bug
    - Ejemplo: `🐛 fix: correct form validation`
  - `docs` → Documentación
    - Ejemplo: `📝 docs: update README`
  - `refactor` → Refactorización de código
    - Ejemplo: `♻️ refactor: simplify login flow`
  - `db` → Cambios en la base de datos
    - Ejemplo: `🗄️ db: add new model Event`

---

## 📐 Convenciones de Desarrollo

- HTML semántico y respetar mockups.
- CSS usando BEM y custom properties.
- Componentes CSS separados en `/components/`.
- JavaScript limpio, con manejo de errores y uso de SweetAlert2 y Notyf.
- Separación de responsabilidades:
  - Views → lógica de presentación
  - Services → lógica de negocio y comunicación con el modelo
  - Models → base de datos
- Formularios dinámicos en `forms.py` por app.
- Componentes reutilizables (inputs, cards, botones, etc.).
- Optimización de imágenes a WebP (TinyPNG o Squoosh).
- Comentarios y código en español (excepto clases CSS).
- Modificar solo los archivos necesarios; cambios mayores deben comunicarse al líder.

---

## 📄 Licencia

Propiedad del equipo SIGEU, uso interno de desarrollo.

---