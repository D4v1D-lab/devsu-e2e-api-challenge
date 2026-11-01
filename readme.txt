README - Ejercicio Devsu (E2E + API)
====================================

Contenido del paquete
---------------------
- E2E: pruebas de interfaz con Selenium WebDriver 4 + Python + pytest (patron Page Object Model).
- API: pruebas de servicios REST con Postman + Newman.
- CI: GitHub Actions ejecuta ambas suites.

Requisitos
----------
- Python 3.10 o superior
- Google Chrome (version estable)
- Node.js 18 o superior y npm
- Git

Ejecucion - E2E
----------------
1. Crear el entorno virtual:
   python3 -m venv .venv
2. Activarlo:
   source .venv/bin/activate        (Linux o macOS)
   .venv\Scripts\activate           (Windows)
3. Instalar dependencias:
   pip install -r requirements.txt
4. Ejecutar las pruebas en modo headless:
   pytest -v
5. Ver el reporte de pytest en reports/.

Ejecucion - API
---------------
1. Entrar a la carpeta:
   cd postman
2. Instalar dependencias:
   npm install
3. Ejecutar la coleccion:
   npm test
4. Reporte HTML generado en reports/newman-report.html

Ejecucion - CI
--------------
El workflow .github/workflows/ci.yml se ejecuta en cada push y pull request.
Deja disponibles los reportes de ambas suites como artefactos descargables.

Empaquetado
-----------
   chmod +x package.sh
   ./package.sh
Genera devsu-exercise.zip sin .git, .venv, __pycache__, node_modules ni reportes.

Notas
-----
- Credenciales de Sauce Demo: standard_user / secret_sauce
- La URL base de la API se puede cambiar con la variable baseUrl de Postman.
