# 🚗 Sistema de Alquiler de Vehículos

Sistema de información desarrollado en **Django** para una empresa de alquiler de vehículos. Permite registrar, desde el panel de administración, los vehículos por categoría, los clientes, cada alquiler con sus fechas, los accesorios alquilados (GPS, silla para bebé) y los mantenimientos realizados a cada vehículo.

> Proyecto 6 · Segundo corte · Programación Avanzada  
> Facultad de Ingeniería · Ingeniería de Sistemas · Universidad de La Guajira

## 👥 Integrantes

| Nombre | Usuario de GitHub |
|---|---|
| _Pedro Villamil_ | [@ING-PEDRO](https://github.com/ING-PEDRO) |
| _Mateo Fonseca_ | [@mateofonseca08-lab](https://github.com/mateofonseca08-lab) |
| _Ender Montero_ | [@EnderMonter](https://github.com/EnderMonter) |

## 🎯 ¿Qué hace el sistema?

- Registra los **vehículos** y los organiza por **categoría** (con su tarifa diaria).
- Registra el **historial de mantenimientos** de cada vehículo.
- Registra los **clientes** (documento, contacto y licencia).
- Registra cada **alquiler** con su cliente, vehículo, fechas y total.
- Registra los **accesorios** disponibles y cuáles (y cuántos) se alquilan en cada alquiler.

Toda la información se gestiona desde el **panel de administración de Django** (`/admin`).

## 🧑‍💼 Actores y casos de uso

| Actor | Casos de uso |
|---|---|
| Administrador | Gestionar usuarios, gestionar categorías, consultar reporte de alquileres |
| Asesor comercial | Registrar cliente, registrar alquiler, asignar accesorios a un alquiler |
| Jefe de flota | Registrar vehículo, registrar mantenimiento, consultar estado de la flota |
| Cliente | Consultar vehículos disponibles, consultar historial de alquileres, actualizar sus datos |



## 🗄️ Modelo de datos

El modelo tiene **7 tablas** y sigue la convención `tbl_` + nombre en singular, `pk_` + prefijo + `_id` para llaves primarias y `fk_` + prefijo de la tabla referenciada + `_id` para llaves foráneas.

| Tabla | Descripción |
|---|---|
| `tbl_categoria` | Categorías de vehículos y su tarifa diaria |
| `tbl_vehiculo` | Vehículos de la flota (placa, marca, modelo, año, estado) |
| `tbl_mantenimiento` | Mantenimientos de cada vehículo (**entidad débil**) |
| `tbl_cliente` | Clientes de la empresa |
| `tbl_alquiler` | Alquileres con fechas y total |
| `tbl_accesorio` | Accesorios disponibles y su precio diario |
| `tbl_alquiler_accesorio` | Tabla intermedia del N:M entre alquiler y accesorio (`aac_cantidad`) |

**Relaciones principales**

- Categoría **1:N** Vehículo
- Vehículo **1:N** Mantenimiento (entidad débil)
- Cliente **1:N** Alquiler
- Vehículo **1:N** Alquiler
- Alquiler **N:M** Accesorio, resuelta con `tbl_alquiler_accesorio`



## 🛠️ Tecnologías

- Python 3.12 o superior
- Django 6.1
- Django REST Framework
- SQLite (base de datos por defecto)

## 📁 Estructura del proyecto

```
sistema-alquiler-de-vehiculos/
├── accesorios/        # Accesorios disponibles
├── alquileres/        # Alquileres y accesorios por alquiler
├── clientes/          # Clientes
├── config/            # settings.py, urls.py, asgi.py, wsgi.py
├── flota/             # Categorías, vehículos y mantenimientos
├── docs/              # Diagramas (actores y entidad-relación)
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## ⚙️ Cómo ejecutarlo

### 1. Clonar el repositorio

```bash
git clone https://github.com/ING-PEDRO/sistema-alquiler-de-vehiculos.git
cd sistema-alquiler-de-vehiculos
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
```

- **Windows:** `venv\Scripts\activate`
- **Linux / macOS:** `source venv/bin/activate`

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar las migraciones

```bash
python manage.py migrate
```

### 5. Iniciar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador: <http://127.0.0.1:8000/admin/>

> El repositorio incluye `db.sqlite3` con datos de prueba (mínimo 3 registros por tabla), por lo que el paso 4 solo aplica si la base se crea desde cero. Si se crea desde cero, se debe crear un superusuario con `python manage.py createsuperuser`.

## 🔑 Acceso al panel de administración

| Campo | Valor |
|---|---|
| URL | http://127.0.0.1:8000/admin/ |
| Usuario | `pedro` |
| Contraseña | `Pedro123` |

## 🧩 Panel de administración

- Todos los modelos están registrados con `list_display`, `search_fields` y `list_filter`.
- Los **mantenimientos** se registran dentro del formulario del vehículo (inline).
- Los **accesorios** de un alquiler se registran dentro del formulario del alquiler (inline sobre `tbl_alquiler_accesorio`).

## 📄 Diagramas

Los diagramas están en la carpeta [`docs/`](docs/):

- `casos-de-usus-uml.drawio`: diagrama de casos de uso UML.
- `diagrama_er.drawio`: diagrama entidad-relación.
