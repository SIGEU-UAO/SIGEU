# SIGEU - Sistema de Gestión de Eventos Universitarios

[![Python](https://img.shields.io/badge/python-3.13.7-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.6-green)](https://www.djangoproject.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-12.02-brightgreen)]()
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
- Librerías JS: Datatables, SweetAlert2, Notyf
- Python-dotenv

---

## ⚙ Requisitos

- Python 3.13.7
- XAMPP / MySQL instalado
- MariaDB versión 12.02
- Git
- Navegador moderno (Chrome, Firefox, Edge)

---

> 💡 **Nota:** Para garantizar compatibilidad con SIGEU, se recomienda usar **XAMPP** con MariaDB versión **12.02** o superior. Algunas instalaciones de XAMPP incluyen versiones antiguas de MariaDB que podrían no funcionar correctamente; en ese caso, se recomienda **actualizar manualmente MariaDB reemplazando los archivos en la carpeta de XAMPP**.

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/SIGEU-UAO/SIGEU.git
cd SIGEU
```

2. Ejecutar el entorno virtual:
```bash
setup.bat
```
Esto creará `env/`, instalará dependencias y activará el entorno virtual.

3. Configurar variables de entorno:
- Copiar `.env.template` como `.env`.
- Agregar la contraseña de la base de datos, la configuracion del correo electrónico y otros valores sensibles.

4. Iniciar XAMPP (Preferiblemente / Puede ser cualquier otro servidor local):
- Iniciar Apache
- Iniciar MySQL

5. Crear la base de datos únicamente y su usuario (desde **phpMyAdmin**, por ejemplo):
- Nombre: definido en `.env` (ej: `sigeu`)
- Usuario: `django-user`
- Conceder todos los permisos

6. Crear migraciones:
```bash
python manage.py makemigrations
```

7. Ejecutar migraciones (Crear tablas de la BD):
```bash
python manage.py migrate
```

8. Crear superusuario (administrador):
```bash
python manage.py createsuperuser
```

9. Iniciar servidor:
```bash
python manage.py runserver
```

10. Acceder a http://127.0.0.1:8000/admin/ e iniciar como administrador
   - Poblar tablas Facultades, Programas, Unidades Academicas e Instalaciones Físicas

11.  Iniciar el recorrido por el software a través de http://127.0.0.1:8000/registro

---

## 📁 Estructura del Proyecto

```
sigeu/
│
├── manage.py
├── .env
├── .env.template
├── .gitignore
├── README.md
├── requirements.txt
├── setup.bat
├── sigeu/
│   ├── settings.py
│   ├── decorators.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/
│   ├── layouts/
│   │   └── dashboard.html
│   └── components/
│   └── errors/
│   │   ├── error.html
├── static/
│   ├── assets/
│   │   ├── img/
│   │   ├── icons/
│   │   └── favicon/
│   ├── css/
│   │   ├── base.css
│   │   ├── dashboard.css
│   │   └── components/
│   └── js/
│       ├── main.js
│       ├── base.js
│       └── modules/
├── apps/
│   └── nombre_app/
│   │   ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── urls.py
│       ├── utils.py
│       ├── services/
│       │   └── <archivo por servicio>.py
│       ├── views.py
│       ├── serializers/ (cuando aplique)
│       │   └── <archivo por serializer>.py
│       ├── validations/ (cuando aplique)
│       │   └── <archivo por validacion>.py
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

```

---

## 🏗 Arquitectura de SIGEU

El sistema está diseñado bajo el patrón **MVT (Model–View–Template)** nativo de Django, complementado con una **Services Layer** adicional que refuerza la separación de responsabilidades y facilita la escalabilidad.

### 🔹 Modelo MVT

- **Models (`models.py`)**  
  Definen la estructura de datos y se comunican con la base de datos mediante el ORM de Django.  
  Ejemplo: usuarios, eventos, organizaciones externas, notificaciones.

- **Views (`views.py`)**  
  Manejan la lógica de presentación. Procesan solicitudes HTTP, interactúan con los *services* y retornan respuestas HTML renderizadas con plantillas DTL (Django Template Language).  

- **Templates (`templates/`)**  
  Contienen la capa de interfaz de usuario. Se basan en layouts reutilizables y componentes modulares (dashboard, formularios, listas, etc.).

### 🔹 Services Layer

Además del esquema clásico MVT, SIGEU implementa una **capa de servicios por aplicación**. Su propósito es centralizar la **lógica de negocio**, de modo que las *views* solo deleguen responsabilidades.  

Ejemplos:
- `apps/users/service.py`: validación de credenciales, recuperación de contraseñas, asignación de roles.
- `apps/events/services/event.py`: gestión de estados (borrador → enviado → aprobado/rechazado), validación de avales PDF, publicación automática de eventos.
- `apps/external_organizations/service.py`: creación, edición y asociación de organizaciones externas

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

---

## 📄 Licencia

Propiedad del equipo SIGEU, uso interno de desarrollo.

---