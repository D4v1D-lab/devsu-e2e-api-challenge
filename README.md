# Devsu E2E + API Challenge

[![CI](https://github.com/D4v1D-lab/devsu-e2e-api-challenge/actions/workflows/ci.yml/badge.svg)](https://github.com/D4v1D-lab/devsu-e2e-api-challenge/actions/workflows/ci.yml)

Ejercicio práctico de QA Automation / SDET:

- **Parte 1** — Pruebas E2E de UI con **Selenium WebDriver 4 + Python + pytest** (Page Object Model) contra [Sauce Demo](https://www.saucedemo.com/).
- **Parte 2** — Pruebas de API con **Postman + Newman** (reporte HTML vía `newman-reporter-htmlextra`).
- **Parte 3** — **GitHub Actions** CI ejecutando ambas suites en push y pull requests.

> **Nota sobre credenciales:** el enunciado del ejercicio puede listar credenciales incorrectas de Sauce Demo.
> Usa las reales: **`standard_user` / `secret_sauce`**.

> **URL base de la API:** `{{baseUrl}}` en la colección de Postman es un **placeholder**.
> Confirma la URL real de la API con el equipo de contratación. Este repositorio usa por defecto `https://api.demoblaze.com` (API demo pública con `/signup` y `/login`) para que la suite sea ejecutable sin configuración adicional.

---

## Estructura del proyecto

```
.
├── .github/workflows/ci.yml      # CI: pytest + Newman
├── pages/                        # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── checkout_complete_page.py
├── tests/                        # Tests de pytest
│   ├── test_login.py             # login válido + inválido
│   └── test_checkout.py          # checkout happy path
├── postman/
│   ├── saucedemo-api.postman_collection.json
│   ├── package.json              # Newman + htmlextra
│   └── package-lock.json
├── reports/                      # screenshots + reporte Newman (generados)
├── conftest.py                   # fixture del driver, screenshot en fallos
├── requirements.txt
├── pytest.ini
├── package.sh                    # zip de los entregables
└── README.md
```

---

## Prerrequisitos

- **Python 3.10+**
- **Google Chrome** (estable)
- **Node.js 18+** y npm (para Newman)
- Git

---

## Parte 1 — E2E (Selenium + pytest)

### Configuración

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecutar los tests

```bash
# Headless (por defecto, apto para CI)
HEADLESS=true pytest

# Con navegador visible (debug local)
HEADLESS=false pytest

# Un solo archivo
pytest tests/test_checkout.py -v
```

Variables de entorno opcionales:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `BASE_URL` | `https://www.saucedemo.com/` | App bajo prueba |
| `HEADLESS` | `true` | Ejecutar Chrome en modo headless |
| `SAUCE_USERNAME` | `standard_user` | Usuario de login |
| `SAUCE_PASSWORD` | `secret_sauce` | Contraseña de login |
| `CHECKOUT_FIRST_NAME` | `John` | Formulario de checkout |
| `CHECKOUT_LAST_NAME` | `Doe` | Formulario de checkout |
| `CHECKOUT_POSTAL_CODE` | `12345` | Formulario de checkout |

### Capturas de pantalla en fallos

Los tests fallidos guardan PNGs en `reports/screenshots/`.

---

## Parte 2 — API (Postman + Newman)

### Configuración

```bash
cd postman
npm install
```

### Ejecutar con Newman + reporte HTML

```bash
cd postman
npm test
```

Esto ejecuta la colección y escribe:

`reports/newman-report.html`

Abre ese archivo en el navegador para ver el reporte.

### Requests de la colección

1. **POST /signup** — éxito (username único vía pre-request script)
2. **POST /login** — credenciales válidas (usa el usuario creado en signup)
3. **POST /login** — credenciales inválidas (espera `errorMessage`)

Todas las URLs usan la variable de colección `{{baseUrl}}` (sin hosts hardcodeados en los requests).

Para apuntar a otro entorno:

```bash
npx newman run saucedemo-api.postman_collection.json \
  --env-var "baseUrl=https://tu-api.ejemplo.com" \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export ../reports/newman-report.html
```

---

## Parte 3 — CI

Workflow: `.github/workflows/ci.yml`

| Job | Qué hace |
|-----|----------|
| `e2e-python` | Instala dependencias → `pytest` headless → sube `reports/` |
| `api-newman` | `npm install` → Newman + htmlextra → sube el reporte HTML |

Triggers: `push` y `pull_request`.

---

## Empaquetado

```bash
chmod +x package.sh
./package.sh
```

Crea `devsu-exercise.zip`, excluyendo `.git`, `.venv`, `__pycache__`, `node_modules` y los reportes generados.

---

## Resumen de cobertura de tests

| Suite | Escenario |
|-------|-----------|
| E2E | Login con credenciales válidas → página de productos |
| E2E | Login con credenciales inválidas → mensaje de error |
| E2E | Agregar 2 productos → carrito → checkout → finish → "THANK YOU FOR YOUR ORDER" |
| API | Signup exitoso |
| API | Login exitoso |
| API | Login fallido (credenciales inválidas) |
