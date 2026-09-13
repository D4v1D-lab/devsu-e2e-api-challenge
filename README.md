# Devsu E2E + API Challenge

[![CI](https://github.com/D4v1D-lab/devsu-e2e-api-challenge/actions/workflows/ci.yml/badge.svg)](https://github.com/D4v1D-lab/devsu-e2e-api-challenge/actions/workflows/ci.yml)

Ejercicio práctico de QA Automation / SDET:

- **Parte 1** — Pruebas E2E de UI con **Selenium WebDriver 4 + Python + pytest** (Page Object Model) contra [Sauce Demo](https://www.saucedemo.com/).
- **Parte 2** — Pruebas de servicios REST con **Postman + Newman** (reporte HTML vía `newman-reporter-htmlextra`) contra la API de [PetStore](https://petstore.swagger.io/).
- **Parte 3** — **GitHub Actions** CI ejecutando ambas suites en push y pull requests.

> **Nota sobre credenciales:** el enunciado del ejercicio puede listar credenciales incorrectas de Sauce Demo.
> Usa las reales: **`standard_user` / `secret_sauce`**.

> **URL base de la API:** `{{baseUrl}}` en la colección de Postman es un **placeholder**.
> Por defecto apunta a la demo pública de PetStore: `https://petstore.swagger.io/v2` (documentación en `https://petstore.swagger.io/`).

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
│   ├── petstore-api.postman_collection.json
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

La colección tiene dos folders:

1. **`Ciclo de vida: crear, actualizar y eliminar un usuario`** — cubre el ciclo de vida completo de un usuario en la API de PetStore:
   1. **POST /user** — Crear un usuario (username único generado en pre-request)
   2. **GET /user/{username}** — Buscar el usuario creado
   3. **PUT /user/{username}** — Actualizar el nombre y el correo del usuario
   4. **GET /user/{username}** — Buscar el usuario actualizado (valida los cambios)
   5. **DELETE /user/{username}** — Eliminar el usuario
   6. **GET /user/{username}** — Verificar la eliminación (espera HTTP 404)
2. **`Defecto documentado: PUT /user con id: 0`** — reproduce un defecto real de la API (ver sección [Defectos encontrados](#defecto-encontrado-put-user-con-id-0-no-actualiza-crea-un-registro-nuevo)). Termina en rojo a propósito.

Todas las URLs usan la variable de colección `{{baseUrl}}` (sin hosts hardcodeados en los requests).

### Variables de la colección

| Variable | Descripción |
|----------|-------------|
| `baseUrl` | URL base de la API (placeholder) |
| `username` | Usuario generado de forma única en cada ejecución |
| `userId` | Id devuelto por el servidor al crear el usuario |
| `firstName`, `lastName`, `email` | Datos originales del usuario |
| `updatedFirstName`, `updatedLastName`, `updatedEmail` | Datos nuevos usados en la actualización |
| `password`, `phone` | Credenciales y teléfono del usuario |

### Defecto encontrado: `PUT /user` con `id: 0` no actualiza, crea un registro nuevo

**Comportamiento esperado:** `PUT /user/{username}` actualiza el recurso identificado por la URL; el `GET` posterior a esa misma URL debe reflejar los cambios.

**Comportamiento real (reproducido con curl y Newman):**

```
POST /user  {"id":0, "username":"qa_check_…", "firstName":"Juan"}
  → 200 {"message":"9223372036854767906"}

PUT /user/qa_check_…  {"id":0, "firstName":"Carlos"}
  → 200 {"message":"9223372036854767907"}      ← id NUEVO, y responde "éxito"

GET /user/qa_check_…  (tres veces)
  → {"id":9223372036854767906, "firstName":"Juan"}   ← nunca se actualizó
```

**Causa:** la URL identifica al usuario; un body con `id: 0` hace que PetStore cree un registro **nuevo** y responda `200`, sin tocar el recurso de la URL. La API responde "éxito" a una operación que no hizo lo que pide su contrato.

**Manejo en la entrega:** el folder `Defecto documentado: PUT /user con id: 0` reproduce el defecto de forma autocontenida (crea su propio usuario de control) y deja la verificación **en rojo a propósito** mientras el defecto exista:

```bash
cd postman
npm run test:defect    # esperado: 3 verdes + 1 rojo (la verificación C)
```

El flujo principal (`npm test`) usa el `userId` real en el PUT — ese es el path correcto — y queda en verde con 16/16 aserciones.

### Hallazgo (positivo): los ids de PetStore superan 2^53

JavaScript representa enteros exactos solo hasta `2^53 − 1` (`9007199254740991`). PetStore devuelve ids como `9223372036854767906`, así que `pm.response.json().id` llegaría **redondeado**. Por eso el id se captura desde `message` (string) y se compara contra el texto crudo de la respuesta. La demo pública de PetStore funciona de forma determinista con este flujo (verificado con Newman, 16/16 aserciones).

Para apuntar a otro entorno:

```bash
npx newman run petstore-api.postman_collection.json \
  --env-var "baseUrl=https://tu-api.ejemplo.com/v2" \
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
| E2E | Login con credenciales inválidas → mensaje de error exacto |
| E2E | Agregar 2 productos → carrito → checkout → finish → "THANK YOU FOR YOUR ORDER" |
| E2E | El carrito y el resumen muestran los productos correctos (Backpack + Bike Light) |
| E2E | El subtotal del resumen es la suma de los precios (29.99 + 9.99) |
| API | Crear un usuario |
| API | Buscar el usuario creado |
| API | Actualizar el nombre y el correo del usuario |
| API | Buscar el usuario actualizado |
| API | Eliminar el usuario |
| API | Verificar la eliminación (404) |
| API | PUT con `id: 0` — reproduce el defecto documentado (en rojo a propósito) |

### Fuera de alcance

- **E2E:** un solo navegador (Chrome headless), un solo usuario (`standard_user`) y sin cubrir a los otros usuarios de Sauce Demo (`locked_out`, `problem`, `performance`). No se prueban ordenamientos, detalle de producto ni pagos reales.
- **API:** solo el recurso `/user` de PetStore; no se cubren pet, store ni la validación del contrato OpenAPI.
- No se ejecutaron pruebas de carga, seguridad ni compatibilidad entre navegadores.

Nadie espera que se pruebe todo; esta sección deja explícito qué no se probó.
