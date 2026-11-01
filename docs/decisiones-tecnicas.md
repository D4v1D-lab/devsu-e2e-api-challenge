# Decisiones tecnicas

Registro breve de por que el proyecto esta armado asi. Sirve para quien revise la entrega.

## E2E
- **Selenium WebDriver + pytest en lugar de Cypress:** el enunciado lista Selenium como framework
  deseable y el equipo mantiene Python para API y SQL; una sola herramienta para ambas capas.
- **Page Object Model:** los localizadores viven en `pages/` y los tests describen el flujo.
  Si cambia un id, se corrige en un solo archivo.
- **Esperas explicitas:** se usan `WebDriverWait` y condiciones (`EC`). Las esperas fijas producian
  fallos intermitentes en headless.
- **Dos productos fijos (Backpack y Bike Light):** el enunciado pide dos productos; se eligen los
  de precio conocido (29.99 y 9.99) para poder verificar el subtotal exacto.

## API
- **Postman + Newman:** permite ejecutar la coleccion desde CI sin instalar un framework adicional.
  El enunciado acepta cualquier herramienta.
- **Variables de coleccion:** `username`, `userId` y `baseUrl` se generan o se leen en tiempo de
  ejecucion; ningun id queda escrito a mano.
- **Id capturado como texto:** los ids de PetStore superan 2^53 y JavaScript los redondearia.
- **Defecto de `PUT /user` con `id: 0` separado en su propia carpeta:** el flujo principal queda en
  verde y la reproduccion del defecto se ejecuta aparte, con su propio usuario de control.

## CI
- **Dos jobs independientes (E2E y API):** si falla una suite, la otra sigue y se ve el resultado
  completo. Los reportes se suben como artefactos incluso cuando el job falla.

## Fuera de alcance
- Sin pruebas de carga, seguridad ni compatibilidad entre navegadores.
- Solo el recurso `/user` de PetStore.
