# Prueba técnica: Mini-crédito

Gracias por tomarte el tiempo. Esta es una app chica de préstamos personales, armada
a medias, parecida a los problemas que resolvemos todos los días: plata, fechas, un
proveedor externo que cobra por consulta y datos personales.

- **Tiempo:** pensada para **3 a 4 horas**. No hace falta terminar todo: preferimos
  pocas cosas bien hechas y bien explicadas.
- **Plazo:** 5 días desde que la recibís.
- **IA:** podés usar Claude, Copilot, Cursor o lo que uses normalmente. Lo que nos
  importa es tu criterio: contanos en `NOTAS.md` qué te sugirió y qué corregiste.
- **Después:** una charla de 45 minutos donde recorremos tu entrega y te pedimos un
  cambio chico en vivo.

## Cómo entregar

1. Arriba a la derecha: **Use this template → Create a new repository**, como
   **privado** en tu cuenta. (No hagas fork: los forks de un repo público son
   públicos.)
2. Trabajá ahí, con commits chicos y mensajes claros. El historial también se lee.
3. Al terminar, invitá a **@leandrogallo** como colaborador y avisanos por mail.

Si no tenés cuenta de GitHub, mandanos un `.zip` del repo **con la carpeta `.git`**.

## Cómo levantarlo

Sólo necesitás **Docker** (Docker Desktop o Docker Engine con Compose v2) y `make`.

```bash
make up         # levanta Postgres, la API y la web
make test       # corre los tests de la API y de la web
make logs       # sigue los logs
make down       # apaga todo
make reset      # borra la base y arranca de cero
```

- API con documentación interactiva: http://localhost:8000/docs
- Web: http://localhost:5173

Al empezar, **2 tests de la API fallan a propósito**: son parte de las tareas.

Si el puerto 8000 o el 5173 están ocupados, cambialos en `docker-compose.yml`. Si
algo no levanta en 10 minutos, escribinos: el problema es nuestro, no tuyo.

## Qué hay

```
api/   Python 3.12 · FastAPI · SQLAlchemy 2 · Postgres 16 · pytest
web/   React 18 · TypeScript · Vite · Vitest + Testing Library
```

- **Login simulado:** el front manda el id del cliente en el header `X-Cliente-Id`.
  Tratalo como si viniera de un token ya validado. Hay tres clientes de prueba: Ana
  (score 820), Bruno (310) y Carla (640).
- **Buró de crédito:** `api/app/buro_falso.py` simula un proveedor externo. **No lo
  modifiques.** Cada consulta tarda y nos cuesta plata; `consultas_cobradas` es lo
  que nos facturaría.
- **Outbox de marketing:** `evento_outbox` guarda los eventos de conversión. Otro
  proceso (fuera de esta prueba) los manda a una plataforma de publicidad.

## Reglas del negocio

- Un cliente puede pedir un préstamo si su score es **500 o más**.
- Plazos de 3, 6 o 12 meses, cada uno con su **monto máximo** y su **TEA**
  (`api/app/config.py`).
- **Comisión administrativa:** 2 % del monto, redondeada al centavo.
- **Una consulta al buró sirve 30 días** para el mismo cliente.
- Operamos en Uruguay: **las fechas de vencimiento son en hora de Montevideo.**
- **Cronograma:** sistema francés (cuota fija).
  - Tasa mensual efectiva = `(1 + TEA) ^ (1/12) - 1`.
  - Montos con 2 decimales, redondeo comercial (0,005 → 0,01).
  - La suma del capital de las cuotas tiene que dar **exactamente** el monto: la
    diferencia de redondeo se ajusta en la última cuota.
  - Vencimientos mensuales, el mismo día que el primero. Si ese día no existe en el
    mes (31 de febrero), vence el último día del mes.

## Tareas

Elegí el orden. Si no llegás a todo, priorizá y contanos en `NOTAS.md` qué dejaste
afuera y por qué.

1. **Crear una oferta bien.** `POST /ofertas` hoy no valida el monto máximo del
   plazo, y si el cliente hace doble clic en «Confirmar» se crean dos ofertas.
   Arreglalo para que **no pueda haber dos ofertas pendientes del mismo cliente**,
   aunque lleguen dos requests al mismo tiempo. Del lado de la web, que tampoco se
   pueda mandar dos veces.
2. **No pagar dos veces al buró.** Cada llamada a elegibilidad o a crear una oferta
   consulta al buró de nuevo. Usá la consulta guardada si tiene menos de 30 días.
3. **Cronograma y atraso.** Implementá `generar_cronograma` en
   `api/app/cronograma.py` según las reglas de arriba, y arreglá `dias_de_atraso`
   (`api/app/atraso.py`), que tiene un test que falla. Agregá los tests que creas
   necesarios.
4. **El borrador de la solicitud.** El formulario de la web guarda un borrador para
   retomarlo. Hoy, si Ana deja un borrador a medias, sale y entra Bruno en la misma
   computadora, Bruno ve el monto, el teléfono y la dirección de Ana. Arreglalo, y
   que el borrador se borre cuando la solicitud se envía. Con tests.
5. **El evento de conversión.** `registrar_conversion` deja un evento «Lead» en el
   outbox cada vez que un cliente elegible consulta su elegibilidad, y lo manda con
   el email y la cédula en claro. Tiene que ser **un solo evento por cliente** y el
   payload no puede llevar datos personales en claro: la plataforma de publicidad
   acepta el email normalizado (minúsculas, sin espacios) y hasheado con SHA-256.
6. **Revisión de código.** En el código que ya existe hay **al menos dos bugs** que
   no están en esta lista. Encontralos y arreglalos (o, si no te da el tiempo,
   explicalos en `NOTAS.md`).
7. **Un gráfico de cómo funciona.** En `DIAGRAMA.md`, en la raíz, uno o dos
   diagramas que le expliquen el sistema a alguien que entra al equipo:
   - las piezas (web, API, base, buró, outbox) y cómo se hablan;
   - qué pasa, paso a paso, desde que el cliente aprieta «Confirmar» hasta que
     tiene su oferta, **con tus cambios ya hechos** (dónde se valida el tope, dónde
     se usa la caché del buró, qué evita la oferta duplicada).

   Recomendamos [Mermaid](https://mermaid.js.org), que GitHub muestra directo en
   el Markdown, pero sirve cualquier herramienta si subís la imagen. No miramos lo
   lindo: miramos que sea correcto y que se entienda.
8. **`NOTAS.md`.** En la raíz, corto:
   - qué hiciste y qué dejaste afuera, y por qué;
   - las decisiones que tomaste y qué alternativas descartaste;
   - qué haría falta para llevar esto a producción;
   - cómo usaste la IA, si la usaste, y qué le corregiste.

## Qué miramos

- Que funcione y tenga tests que prueben lo que importa.
- Cómo manejás plata, fechas y concurrencia.
- Datos personales: qué guardás, qué logueás, qué mandás afuera.
- Código claro, que se entienda sin vos al lado.
- Tu criterio para priorizar y explicar, en `NOTAS.md` y en el diagrama.

No miramos: diseño visual, cantidad de líneas ni que uses tal o cual librería.

¡Suerte! Cualquier duda, escribinos.
