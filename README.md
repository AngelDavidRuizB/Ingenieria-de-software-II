# Taller Postman y graphql

> **Curso:** Ingeniería de Software — Universidad Nacional de Colombia (FCE)

---

## Tabla de contenido

- [Parte 1 — API REST: SpaceX API](#parte-1--api-rest-spacex-api)
  - [¿Qué API elegiste y por qué?](#qué-api-elegiste-y-por-qué)
  - [¿Qué datos devuelve?](#qué-datos-devuelve)
  - [¿Usa token o no?](#usa-token-o-no-qué-tipo)
  - [Requests de la colección](#requests-de-la-colección)
  - [Códigos de estado recibidos](#códigos-de-estado-recibidos)
  - [¿Qué aprendiste diferente a JSONPlaceholder?](#qué-aprendiste-diferente-a-jsonplaceholder)
- [Parte 2 — GraphQL: Countries API](#parte-2--graphql-countries-api)
  - [Queries de la colección](#queries-de-la-colección)
  - [Tests automáticos](#tests-automáticos)
  - [GraphQL vs REST](#graphql-vs-rest)
  - [Requests REST equivalentes a la query más compleja](#requests-rest-equivalentes-a-la-query-más-compleja)
  - [¿En qué proyecto real usarías GraphQL?](#en-qué-proyecto-real-usarías-graphql)
- [Entregables](#entregables)

---

## Parte 1 — API REST: SpaceX API

**Base URL:** `https://api.spacexdata.com/v4`

### ¿Qué API elegiste y por qué?

Se eligió la **SpaceX API v4** por las siguientes razones:

- No requiere registro ni token de ningún tipo, lo que elimina fricción para comenzar el ejercicio.
- Cuenta con múltiples recursos relacionados (lanzamientos, cohetes, payloads) que permiten practicar GET de colecciones, GET por ID y POST de consultas con filtros.
- Sus respuestas tienen estructuras complejas y reales: fechas ISO 8601, arrays de IDs de referencia, objetos anidados y valores nulos, lo que supera en riqueza a JSONPlaceholder.
- Soporta un endpoint especial `POST /launches/query` con filtros y paginación tipo MongoDB, ideal para practicar requests con body JSON.

---

### ¿Qué datos devuelve?

Cada objeto de lanzamiento contiene entre otros:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `string (UUID)` | Identificador único del lanzamiento |
| `name` | `string` | Nombre de la misión |
| `date_utc` | `ISO 8601` | Fecha y hora del lanzamiento en UTC |
| `success` | `boolean` | Si el lanzamiento fue exitoso |
| `rocket` | `string (ref ID)` | ID del cohete usado (relación externa) |
| `payloads` | `array de IDs` | IDs de las cargas útiles transportadas |
| `links.patch.small` | `string (URL)` | URL del parche oficial de la misión |
| `details` | `string \| null` | Descripción narrativa del lanzamiento |

---

### ¿Usa token o no? ¿Qué tipo?

**No usa token.** La SpaceX API v4 es completamente pública. No se envía ningún header de autenticación, API Key ni token de ningún tipo. Todos los endpoints responden sin credenciales.

Esto contrasta, por ejemplo, con The Lord of the Rings API (que usa `Authorization: Bearer <token>`) o la SuperHero API (que embebe el token directamente en la URL).

---

### Requests de la colección

#### Request 1 — GET All Launches

```
GET https://api.spacexdata.com/v4/launches
```

Obtiene la lista completa de todos los lanzamientos históricos y futuros de SpaceX. Responde con un array JSON donde cada elemento tiene más de 30 campos.

**Tests automáticos:**
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Response is an array", () => pm.expect(pm.response.json()).to.be.an('array'));
pm.test("Array is not empty", () => pm.expect(pm.response.json().length).to.be.greaterThan(0));
pm.test("Each item has an id field", () => pm.expect(pm.response.json()[0]).to.have.property('id'));
```

---

#### Request 2 — GET Launch by ID

```
GET https://api.spacexdata.com/v4/launches/5eb87cd9ffd86e000604b32a
```

Obtiene el detalle de un lanzamiento específico por su UUID. El ID usado corresponde al primer lanzamiento histórico de SpaceX: **Falcon 1 DemoFlight 1 (2006)**. Practica el patrón `GET /resource/:id`.

**Tests automáticos:**
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Response has name field", () => pm.expect(pm.response.json()).to.have.property('name'));
pm.test("Response has date_utc field", () => pm.expect(pm.response.json()).to.have.property('date_utc'));
```

---

#### Request 3 — GET Latest Launch

```
GET https://api.spacexdata.com/v4/launches/latest
```

Sub-recurso especial que devuelve directamente el objeto del lanzamiento más reciente sin necesidad de conocer su ID. Practica el acceso a sub-recursos con nombre semántico.

**Tests automáticos:**
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Response has success field", () => pm.expect(pm.response.json()).to.have.property('success'));
pm.test("Response is a single object", () => pm.expect(Array.isArray(pm.response.json())).to.be.false);
```

---

#### Request 4 — GET All Rockets (con Query Params)

```
GET https://api.spacexdata.com/v4/rockets?active=true
```

Lista todos los cohetes de SpaceX. Se añade el query param `active=true` en la pestaña **Params** de Postman. Devuelve objetos con campos como `name`, `country`, `first_flight`, `success_rate_pct`, `mass`, `stages`, etc.

**Tests automáticos:**
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Response is a non-empty array", () => {
  pm.expect(pm.response.json()).to.be.an('array');
  pm.expect(pm.response.json().length).to.be.greaterThan(0);
});
pm.test("Response time < 3000ms", () => pm.expect(pm.response.responseTime).to.be.below(3000));
```

---

#### Request 5 — POST Query Launches (Filtro Avanzado)

```
POST https://api.spacexdata.com/v4/launches/query
Content-Type: application/json
```

Body:
```json
{
  "query": { "success": true },
  "options": {
    "limit": 5,
    "sort": { "date_utc": "desc" },
    "select": ["name", "date_utc", "success", "details", "rocket"]
  }
}
```

Endpoint especial de consulta tipo MongoDB. Devuelve un objeto con campo `docs` (array de resultados) y metadata de paginación (`totalDocs`, `totalPages`, `page`). Practica `POST` con body JSON y el patrón *query by POST*.

**Tests automáticos:**
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Response has docs array", () => pm.expect(pm.response.json()).to.have.property('docs'));
pm.test("Docs respects limit of 5", () => pm.expect(pm.response.json().docs.length).to.be.at.most(5));
pm.test("All launches are successful", () => {
  pm.response.json().docs.forEach(l => pm.expect(l.success).to.be.true);
});
pm.test("Response has pagination metadata", () => {
  pm.expect(pm.response.json()).to.have.property('totalDocs');
  pm.expect(pm.response.json()).to.have.property('totalPages');
});
```

---

### Códigos de estado recibidos

| Request | Método | Código | Significado |
|---|---|---|---|
| GET All Launches | GET | `200 OK` | Colección devuelta correctamente |
| GET Launch by ID | GET | `200 OK` | Recurso encontrado por ID |
| GET Latest Launch | GET | `200 OK` | Sub-recurso especial devuelto |
| GET All Rockets | GET | `200 OK` | Lista con query param procesada |
| POST Query Launches | POST | `200 OK` | Consulta con filtro ejecutada |

> **Nota:** Un ID inexistente devuelve `404 Not Found`. Un body mal formado en el POST devuelve `400 Bad Request`.

---

### ¿Qué aprendiste diferente a JSONPlaceholder?

- **Datos reales y complejos:** JSONPlaceholder devuelve objetos ficticios simples (4-5 campos). SpaceX devuelve objetos con más de 30 campos, fechas ISO 8601, arrays de IDs relacionales y URLs embebidas.
- **Sub-recursos semánticos:** Endpoints como `/launches/latest` y `/launches/upcoming` no existen en JSONPlaceholder. Permiten consultas comunes sin necesidad de filtrar manualmente.
- **Patrón Query by POST:** El endpoint `POST /launches/query` introduce filtrado a través del body (estilo MongoDB), un patrón común en APIs avanzadas que JSONPlaceholder no implementa.
- **Relaciones reales entre recursos:** Un lanzamiento referencia un cohete por UUID y múltiples payloads por IDs, simulando una base de datos relacional real. En JSONPlaceholder los recursos son independientes.
- **Paginación real:** La respuesta del POST incluye `totalDocs`, `totalPages` y `hasNextPage`, algo que JSONPlaceholder no provee en ningún endpoint.

---

## Parte 2 — GraphQL: Countries API

**Endpoint:** `https://countries.trevorblades.com/graphql`  
**Método de todos los requests:** `POST`  
**Body type en Postman:** `GraphQL`

---

### Queries de la colección

#### Query 1 — Todos los continentes

```graphql
query GetAllContinents {
  continents {
    code
    name
  }
}
```

Lista todos los continentes disponibles. Demuestra el uso básico de GraphQL: un solo endpoint y selección explícita de campos.

---

#### Query 2 — Todos los países

```graphql
query GetAllCountries {
  countries {
    code
    name
    capital
    currency
    phone
  }
}
```

Lista todos los países del mundo seleccionando solo 5 de los campos disponibles. Demuestra que GraphQL elimina el *over-fetching*: el servidor devuelve únicamente lo solicitado.

---

#### Query 3 — País por código (argumento) ✅

```graphql
query GetCountryByCode($code: ID!) {
  country(code: $code) {
    name
    capital
    currency
    emoji
    native
  }
}
```

**Variables:**
```json
{ "code": "CO" }
```

Cumple el requisito de **query con filtro por argumento**. Usa una variable GraphQL tipada (`$code: ID!`) para parametrizar la consulta. Resultado: Colombia 🇨🇴.

---

#### Query 4 — Continente con países e idiomas (anidada) ✅

```graphql
query GetContinentWithCountries {
  continent(code: "SA") {
    name
    countries {
      name
      capital
      currency
      languages {
        name
        native
      }
    }
  }
}
```

Cumple el requisito de **query anidada con datos relacionados**. Traversa 3 niveles: `continent → countries → languages`. En REST equivaldría a ~13 requests separados. Con GraphQL es **1 solo request**.

---

#### Query 5 — Idiomas de un país (variable + anidado)

```graphql
query GetCountryLanguages($code: ID!) {
  country(code: $code) {
    name
    languages {
      code
      name
      native
      rtl
    }
  }
}
```

**Variables:**
```json
{ "code": "JP" }
```

Combina variable GraphQL con relación anidada. El campo `rtl` (right-to-left) es booleano — para el japonés es `false`. Resultado: Japan 🇯🇵.

---

### Tests automáticos

Estructura común aplicada en todos los requests (mínimo 3 por request):

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("No GraphQL errors", function () {
    const json = pm.response.json();
    pm.expect(json).to.not.have.property('errors');
});

pm.test("Data property exists", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property('data');
});
```

Adicionalmente cada query tiene tests específicos, por ejemplo para la Query 4:

```javascript
pm.test("Continent SA exists in response", function () {
    const json = pm.response.json();
    pm.expect(json.data.continent.name).to.equal('South America');
});

pm.test("Countries have nested languages array", function () {
    const firstCountry = pm.response.json().data.continent.countries[0];
    pm.expect(firstCountry.languages).to.be.an('array');
});
```

---

### GraphQL vs REST

| Característica | REST | GraphQL |
|---|---|---|
| Número de endpoints | Uno por recurso (`/countries`, `/continents`…) | Un único endpoint `/graphql` |
| Control de campos | El servidor decide qué devolver (*over-fetching*) | El cliente selecciona exactamente qué campos recibe |
| Datos relacionados | Requiere múltiples requests encadenados | Una sola query puede traversar relaciones anidadas |
| Documentación | Manual o separada (Swagger, README) | Schema autodocumentado via introspection |
| Versionado | Endpoints nuevos por versión (`/v1`, `/v2`) | El schema evoluciona sin versiones |
| Depuración en Postman | Body vacío en GETs | Body GraphQL con query y variables separadas |

---

### Requests REST equivalentes a la query más compleja

La **Query 4** (`GetContinentWithCountries`) obtiene en un solo request:
- El nombre del continente Sudamérica
- Sus 12 países con capital y moneda
- Los idiomas de cada uno de esos 12 países

En REST esto requeriría:

1. `GET /continent/SA` → obtener el continente y su lista de países (1 request)
2. `GET /country/{code}` × 12 → detalle de cada país de Sudamérica (12 requests)

**Total REST: 13 requests** → **Total GraphQL: 1 request** (reducción del 92%)

---

### ¿En qué proyecto real usarías GraphQL?

En el **frontend Angular de badges digitales de la UIFCE** sería ideal. Cuando se carga el perfil de un estudiante, la vista necesita simultáneamente:

- Los datos del usuario
- Sus badges emitidos
- Las categorías de esos badges
- El emisor (issuer) de cada badge

Con REST actual esto implica 4 llamadas encadenadas y over-fetching de campos no usados. Con GraphQL, una sola query con los campos exactos que necesita cada componente Angular (usando signals de Angular 21 para reactividad) reduciría la latencia percibida, eliminaría el over-fetching de datos y haría el código del servicio más declarativo y fácil de mantener.

---

## Entregables

| Archivo | Descripción |
|---|---|
| `SpaceX_API_REST_Postman.json` | Colección Postman — 5 requests REST con tests automáticos |
| `GraphQL_Countries_Postman.json` | Colección Postman — 5 queries GraphQL con tests automáticos |
| `Tarea1_APIs_REST_GraphQL.docx` | Documento Word con capturas y análisis completo |
| `README.md` | Este archivo |
