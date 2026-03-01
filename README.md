# AlkeWallet — Billetera Virtual Django

## Estructura del proyecto

```
AlkeSolutions/
├── manage.py
├── requirements.txt
├── AlkeSolutions/              ← Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── AlkeWallet/                 ← App principal
    ├── models.py           ← Wallet, Transaction, Contact
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── admin.py
    └── templates/wallet/
        ├── base.html       ← Base + menú lateral integrado
        ├── index.html      ← Landing page pública
        ├── login.html
        ├── registro.html
        ├── dashboard.html  ← Panel principal
        ├── deposito.html
        ├── envio_dinero.html
        ├── transacciones.html
        └── contactos.html
```

## Instalación y puesta en marcha

### 1. Crear entorno virtual
```bash
python -m venv evirtual
source evirtual/bin/activate        # Linux/Mac
source evirtual\Scripts\activate    # Windows
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario (opcional, para el admin)
```bash
python manage.py createsuperuser
```

### 5. Correr el servidor
```bash
python manage.py runserver
```

### 6. Abrir en el navegador
- **Landing:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## Modelos

| Modelo | Descripción |
|--------|-------------|
| `Wallet` | Billetera asociada 1:1 a cada usuario. Saldo + número de cuenta. |
| `Transaction` | Registro de depósitos, envíos y recepciones. |
| `Contact` | Contactos guardados por usuario para envíos rápidos. |

## URLs

| URL | Vista |
|-----|-------|
| `/` | Landing (index) |
| `/registro/` | Crear cuenta |
| `/login/` | Iniciar sesión |
| `/logout/` | Cerrar sesión |
| `/dashboard/` | Panel principal |
| `/deposito/` | Depositar fondos |
| `/envio/` | Enviar dinero |
| `/transacciones/` | Historial filtrable |
| `/contactos/` | Gestión de contactos |
| `/admin/` | Panel de administración |
