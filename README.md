# TaskMaster

TaskMaster es una aplicación web construida con **Django** que
implementa un sistema de gestión de tareas (to-do lists).\
El objetivo principal es aplicar el patrón **MVC/MTV** en Django y
practicar el modelado de objetos del dominio.

------------------------------------------------------------------------

##  Características principales (MVP)

-   Autenticación de usuarios (login, logout, registro).
-   CRUD completo de **Tareas**.
-   Organización mediante **Listas**.
-   Etiquetado mediante **Categorías**.
-   Campos de **estado**, **prioridad**, y fechas de vencimiento.
-   Panel de administración de Django para gestión interna.

------------------------------------------------------------------------

##  Estructura del proyecto

-   **taskmaster/** → Configuración principal del proyecto (settings,
    urls, wsgi).
-   **tasks/** → App principal con modelos, vistas, urls y templates.
-   **templates/** → Carpeta de plantillas compartidas (base, auth,
    etc).
-   **db.sqlite3** → Base de datos por defecto (puede cambiarse en
    settings).

------------------------------------------------------------------------

##  Requisitos

-   Python 3.11+ (recomendado).
-   Django 5.x.
-   Base de datos SQLite (default), fácilmente reemplazable por
    PostgreSQL/MySQL.
-   VS Code (opcional) con extensiones:
    -   *Django*
    -   *Python*
    -   *GitLens*
    -   *Copilot* (si está disponible).

------------------------------------------------------------------------

## Comandos clave

-   Crear migraciones:

    ``` bash
    python manage.py makemigrations
    ```

-   Aplicar migraciones:

    ``` bash
    python manage.py migrate
    ```

-   Crear superusuario:

    ``` bash
    python manage.py createsuperuser
    ```

-   Levantar servidor:

    ``` bash
    python manage.py runserver
    ```

------------------------------------------------------------------------

## Modelo de Dominio 

``` mermaid
classDiagram
class Usuario
class Administrador
class Lista
class Tarea
class Categoria
class Prioridad
class Recordatorio
class Notificacion
class Progreso
class Reporte

Usuario -- Lista
Usuario -- Tarea
Usuario -- Progreso
Usuario -- Reporte

Administrador -- Usuario

Lista -- Tarea
Tarea -- Categoria
Tarea -- Prioridad
Tarea -- Recordatorio
Recordatorio -- Notificacion

Progreso -- Tarea
Reporte -- Progreso
```

------------------------------------------------------------------------

### Rutas principales

- **Autenticación (Django built-in)**  
  - `/accounts/login/` → Iniciar sesión  
  - `/accounts/logout/` → Cerrar sesión (vista propia en `/tasks/logout/`)  
  - `/tasks/signup/` → Registro de usuarios  

- **Tareas**  
  - `/tasks/` → Listar tareas  
  - `/tasks/create/` → Crear tarea  
  - `/tasks/<id>/` → Detalle de tarea  
  - `/tasks/<id>/edit/` → Editar tarea  
  - `/tasks/<id>/delete/` → Eliminar tarea  
  - `/tasks/<id>/complete/` → Marcar tarea como completada  

- **Listas**  
  - `/tasks/lists/` → Listar listas  
  - `/tasks/lists/create/` → Crear lista  
  - `/tasks/lists/<id>/` → Detalle de lista (con sus tareas)  
  - `/tasks/lists/<id>/edit/` → Editar lista  
  - `/tasks/lists/<id>/delete/` → Eliminar lista  

- **Categorías**  
  - `/tasks/categories/` → Listar categorías  
  - `/tasks/categories/create/` → Crear categoría  
  - `/tasks/categories/<id>/edit/` → Editar categoría  
  - `/tasks/categories/<id>/delete/` → Eliminar categoría  

- **Admin**  
  - `/admin/` → Panel de administración de Django  


------------------------------------------------------------------------

## Estado actual

-   Proyecto inicializado (`taskmaster`).
-   App principal (`tasks`) creada.
-   Modelos y migraciones aplicadas.
-   CRUD básico de Tareas, Listas y Categorías en progreso.
-   Login, logout y registro implementados con vistas propias.

Estos usuarios están preconfigurados para ingresar al sistema:

- **Superusuario**  
  - Usuario: `pipe`  
  - Contraseña: `191311`

- **Usuario de prueba 1**  
  - Usuario: `test1`  
  - Contraseña: `usuarioprueba1`