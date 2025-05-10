# 💰 Sistema de Finanzas Personales

Aplicación web desarrollada con Flask que permite registrar, gestionar y visualizar ingresos y gastos de manera sencilla. Ideal para llevar el control de tus finanzas personales.

## ✨ Características

- 🔐 **Autenticación de usuarios**: Registro, inicio y cierre de sesión.
- 💼 **Gestión de movimientos**: Registrar, editar y eliminar ingresos y gastos.
- 📊 **Resumen financiero**: Balance mensual con ingresos y gastos totales.
- 📈 **Gráficos interactivos**: Comparaciones y distribución por categoría con Chart.js.
- 🔎 **Filtros avanzados**: Por tipo de movimiento, mes y año.
- 💻 **Interfaz moderna**: Diseño responsivo con Bootstrap.

## 📁 Estructura del Proyecto

```
Finanzas-App/
├── app.py
├── run.py
├── requirements.txt
├── BD/
│   └── schema.sql
├── conexion/
│   └── db.py
├── controllers/
│   ├── auth_controller.py
│   └── finance_controller.py
├── routers/
│   ├── auth_routes.py
│   └── finance_routes.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── img/
│   └── js/
│       └── scripts.js
├── styles/
│   └── globals.css
└── templates/
    ├── dashboard.html
    ├── editar_movimiento.html
    ├── layout.html
    ├── login.html
    ├── movimientos.html
    ├── nuevo_movimiento.html
    └── register.html
```

## 🛠️ Requisitos

- Python 3.10 o superior
- MySQL
- Entorno virtual (opcional pero recomendado)

## ⚙️ Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/finanzas-app.git
   cd finanzas-app
   ```

2. (Opcional) Crea y activa un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura la base de datos:
   Crea una base de datos en MySQL y ejecuta el script:
   ```
   BD/schema.sql
   ```

5. Ejecuta la aplicación:
   ```
   python run.py
   ```

6. Accede desde tu navegador:
   ```
   http://127.0.0.1:5000
   ```

## 🚀 Uso

- **Registro**: Crea una cuenta con tu nombre, correo y contraseña.
- **Inicio de sesión**: Accede con tus credenciales.
- **Dashboard**: Visualiza el resumen de tus finanzas.
- **Registrar movimiento**: Ingresa ingresos o gastos con detalle.
- **Editar/eliminar**: Gestiona tus movimientos existentes.
- **Filtros**: Filtra por tipo, mes o año para análisis específico.

## 🧰 Tecnologías Utilizadas

- **Backend**: Flask
- **Base de datos**: MySQL
- **Frontend**: Bootstrap, HTML, CSS, JavaScript, (interfaz 100% responsiva).
- **Gráficos**: Chart.js

## 📸 Capturas de Pantalla

![image](https://github.com/user-attachments/assets/5cf215f1-210d-4e93-917f-ebc1efae9622)
![image](https://github.com/user-attachments/assets/9c74af4c-ecdd-40e6-b933-f2c5e4933d87)
![image](https://github.com/user-attachments/assets/3cef21e0-7d47-4383-8fb4-eac582b9b164)
![image](https://github.com/user-attachments/assets/af8c7027-1e28-4b05-8102-177ec4bb287c)
![image](https://github.com/user-attachments/assets/cecaeca8-76d0-40ae-af8e-50852d28b3ff)
![image](https://github.com/user-attachments/assets/9b872577-b9f8-411d-850d-2f5c958147ef)

## 👤 Autores

- Desarrollado por **Jhonatan Barrera**
  - GitHub: [@jhonatan2405](https://github.com/jhonatan2405)

- Desarrollado por **Juan Arguelles**
  - GitHub: [@juanxpz1](https://github.com/juanxpz1)

- Desarrollado por **Juan De la Espriella**
  - GitHub: [@juanluis-xo](https://github.com/juanluis-xo)



