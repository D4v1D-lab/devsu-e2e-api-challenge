# Devsu E2E + API Challenge

[![CI](https://github.com/D4v1D-lab/devsu-e2e-api-challenge/actions/workflows/ci.yml/badge.svg)](https://github.com/D4v1D-lab/devsu-e2e-api-challenge/actions/workflows/ci.yml)

QA Automation / SDET take-home exercise:

- **Part 1** — End-to-end UI tests with **Selenium WebDriver 4 + Python + pytest** (Page Object Model) against [Sauce Demo](https://www.saucedemo.com/).
- **Part 2** — API tests with **Postman + Newman** (HTML report via `newman-reporter-htmlextra`).
- **Part 3** — **GitHub Actions** CI running both suites on push and pull requests.

> **Credentials note:** The exercise statement may list incorrect Sauce Demo credentials.  
> Use the real ones: **`standard_user` / `secret_sauce`**.

> **API base URL:** `{{baseUrl}}` in the Postman collection is a **placeholder**.  
> Confirm the real API URL with the hiring team. This repo defaults to `https://api.demoblaze.com` (public demo API with `/signup` and `/login`) so the suite is runnable out of the box.

---

## Project structure

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
├── tests/                        # pytest tests
│   ├── test_login.py             # valid + invalid login
│   └── test_checkout.py          # happy-path checkout
├── postman/
│   ├── saucedemo-api.postman_collection.json
│   └── package.json              # Newman + htmlextra
├── reports/                      # screenshots + Newman HTML (generated)
├── conftest.py                   # driver fixture, screenshot on failure
├── requirements.txt
├── pytest.ini
├── package.sh                    # zip deliverables
└── README.md
```

---

## Prerequisites

- **Python 3.10+**
- **Google Chrome** (stable)
- **Node.js 18+** and npm (for Newman)
- Git

---

## Part 1 — E2E (Selenium + pytest)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run tests

```bash
# Headless (default, CI-friendly)
HEADLESS=true pytest

# Headed (local debugging)
HEADLESS=false pytest

# Single file
pytest tests/test_checkout.py -v
```

Optional environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://www.saucedemo.com/` | App under test |
| `HEADLESS` | `true` | Run Chrome headless |
| `SAUCE_USERNAME` | `standard_user` | Login user |
| `SAUCE_PASSWORD` | `secret_sauce` | Login password |
| `CHECKOUT_FIRST_NAME` | `John` | Checkout form |
| `CHECKOUT_LAST_NAME` | `Doe` | Checkout form |
| `CHECKOUT_POSTAL_CODE` | `12345` | Checkout form |

### Screenshots on failure

Failed tests save PNGs under `reports/screenshots/`.

---

## Part 2 — API (Postman + Newman)

### Setup

```bash
cd postman
npm install
```

### Run with Newman + HTML report

```bash
cd postman
npm test
```

This runs the collection and writes:

`reports/newman-report.html`

Open that file in a browser to view the report.

### Collection requests

1. **POST /signup** — success (unique username via pre-request script)
2. **POST /login** — valid credentials (uses user from signup)
3. **POST /login** — invalid credentials (expects `errorMessage`)

All URLs use the collection variable `{{baseUrl}}` (no hardcoded hosts in requests).

To point at another environment:

```bash
npx newman run saucedemo-api.postman_collection.json \
  --env-var "baseUrl=https://your-api.example.com" \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export ../reports/newman-report.html
```

---

## Part 3 — CI

Workflow: `.github/workflows/ci.yml`

| Job | What it does |
|-----|----------------|
| `e2e-python` | Install deps → `pytest` headless → upload `reports/` |
| `api-newman` | `npm install` → Newman + htmlextra → upload HTML report |

Triggers: `push` and `pull_request`.

After you push to GitHub, update the CI badge URL at the top of this README (`OWNER` → your user/org).

---

## Packaging

```bash
chmod +x package.sh
./package.sh
```

Creates `devsu-exercise.zip`, excluding `.git`, `.venv`, `__pycache__`, `node_modules`, and generated reports.

---

## Test coverage summary

| Suite | Scenario |
|-------|----------|
| E2E | Login with valid credentials → products page |
| E2E | Login with invalid credentials → error message |
| E2E | Add 2 products → cart → checkout → finish → "THANK YOU FOR YOUR ORDER" |
| API | Signup success |
| API | Login success |
| API | Login failure (invalid credentials) |
