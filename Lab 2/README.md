# Laboratorio 2 - Segunda Parte: API ToDo con JWT

## Descripcion
Segunda parte del laboratorio de Ingenieria de Software II: Implementacion y validacion de los endpoints **PUT** y **DELETE** para una API ToDo con autenticacion JWT emulada, sin dependencias externas.

## Tecnologias Utilizadas
- **Node.js** (sin dependencias externas)
- **crypto** (modulo nativo para HMAC-SHA256)
- **JWT emulado** con codificacion Base64URL y firma HMAC
- **PowerShell** para pruebas de endpoints
- **HTTP nativo** de Node.js

## Endpoints Implementados

| Metodo | Ruta | Descripcion | Autenticacion |
|--------|------|-------------|---------------|
| POST | `/auth/register` | Registro de usuarios | No |
| POST | `/auth/login` | Login y generacion de token | No |
| GET | `/tasks` | Listar tareas del usuario | Si (Bearer Token) |
| POST | `/tasks` | Crear nueva tarea | Si (Bearer Token) |
| PUT | `/tasks/:id` | Actualizar tarea | Si (Bearer Token) |
| DELETE | `/tasks/:id` | Eliminar tarea | Si (Bearer Token) |

## Implementacion de PUT y DELETE

### PUT `/tasks/:id`
```javascript
if (method === 'PUT' && url.startsWith('/tasks/')) {
  const usuario = autenticar(req);
  if (!usuario)
    return send(res, 401, { error: 'Token requerido o invalido' });

  const id   = url.split('/')[2];
  const idx  = db.tasks.findIndex(t => t.id === id);

  if (idx === -1)
    return send(res, 404, { error: 'Tarea no encontrada' });

  if (db.tasks[idx].userId !== usuario.userId)
    return send(res, 403, { error: 'No tienes permiso para modificar esta tarea' });

  const { title, description, status } = await readBody(req);
  if (title)       db.tasks[idx].title       = title;
  if (description) db.tasks[idx].description = description;
  if (status)      db.tasks[idx].status      = status;

  return send(res, 200, db.tasks[idx]);
}
```

**Logica:**
1. Autenticar al usuario mediante el token Bearer
2. Extraer el ID de la URL
3. Buscar la tarea en la base de datos en memoria
4. Retornar `404` si la tarea no existe
5. Verificar que el usuario sea el dueño de la tarea, retornar `403` si no
6. Leer el body y actualizar solo los campos proporcionados
7. Retornar la tarea actualizada con status `200`

### DELETE `/tasks/:id`
```javascript
if (method === 'DELETE' && url.startsWith('/tasks/')) {
  const usuario = autenticar(req);
  if (!usuario)
    return send(res, 401, { error: 'Token requerido o invalido' });

  const id  = url.split('/')[2];
  const idx = db.tasks.findIndex(t => t.id === id);

  if (idx === -1)
    return send(res, 404, { error: 'Tarea no encontrada' });

  if (db.tasks[idx].userId !== usuario.userId)
    return send(res, 403, { error: 'No tienes permiso para eliminar esta tarea' });

  db.tasks.splice(idx, 1);
  res.writeHead(204);
  return res.end();
}
```

**Logica:**
1. Autenticar al usuario mediante el token Bearer
2. Extraer el ID de la URL
3. Buscar la tarea en la base de datos en memoria
4. Retornar `404` si la tarea no existe
5. Verificar que el usuario sea el dueño de la tarea, retornar `403` si no
6. Eliminar la tarea del arreglo con `splice`
7. Retornar status `204` sin body

## Validacion de Endpoints

### 1. Registro de Usuario
```powershell
Invoke-RestMethod -Method POST -Uri http://localhost:3000/auth/register `
  -ContentType "application/json" `
  -Body '{"username":"ana","email":"ana@test.com","password":"1234"}'
```

**Respuesta:**
```json
{
  "message": "Usuario creado",
  "userId": "1778129173295"
}
```

### 2. Login y Obtencion de Token
```powershell
$token = (Invoke-RestMethod -Method POST -Uri http://localhost:3000/auth/login `
  -ContentType "application/json" `
  -Body '{"email":"ana@test.com","password":"1234"}').token
```

**Respuesta:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxNzc4MTI5MTczMjk1IiwidXNlcm5hbWUiOiJhbmEiLCJleHAiOjE3NzgxMzI3NzY3MTB9.GTnTvLfdYfPkGAqQ709MjM7RfVKyTFQvyEg84wMgrPw"
}
```

### 3. Crear Tarea de Prueba
```powershell
$tarea = Invoke-RestMethod -Method POST -Uri http://localhost:3000/tasks `
  -ContentType "application/json" `
  -Headers @{Authorization="Bearer $token"} `
  -Body '{"title":"Tarea de prueba","description":"Para probar PUT y DELETE"}'
```

**Respuesta:**
```json
{
  "id": "1778129182768",
  "title": "Tarea de prueba",
  "description": "Para probar PUT y DELETE",
  "status": "pending",
  "userId": "1778129173295",
  "createdAt": "2026-05-07T04:46:22.768Z"
}
```

### 4. Validar PUT - Actualizar Estado
```powershell
Invoke-RestMethod -Method PUT -Uri http://localhost:3000/tasks/$($tarea.id) `
  -ContentType "application/json" `
  -Headers @{Authorization="Bearer $token"} `
  -Body '{"status":"completed"}'
```

**Respuesta:**
```json
{
  "id": "1778129182768",
  "title": "Tarea de prueba",
  "description": "Para probar PUT y DELETE",
  "status": "completed",
  "userId": "1778129173295",
  "createdAt": "2026-05-07T04:46:22.768Z"
}
```

### 5. Validar DELETE - Eliminar Tarea
```powershell
Invoke-RestMethod -Method DELETE -Uri http://localhost:3000/tasks/$($tarea.id) `
  -Headers @{Authorization="Bearer $token"}
```

**Respuesta:** `HTTP 204 No Content` (sin body)

### 6. Verificacion Final - Lista de Tareas
```powershell
Invoke-RestMethod -Method GET -Uri http://localhost:3000/tasks `
  -Headers @{Authorization="Bearer $token"}
```

**Respuesta:**
```json
{
  "tasks": []
}
```

## Acceso Remoto

### Configuracion
El servidor fue configurado para escuchar en todas las interfaces de red:

```javascript
server.listen(3000, '0.0.0.0', () => {
  console.log('Servidor corriendo en http://localhost:3000');
  console.log('Acceso remoto habilitado en 0.0.0.0:3000');
});
```

### Prueba de Conexion Remota
Para consumir la API desde otro dispositivo en la misma red (laboratorios de la Universidad Nacional):

1. **Obtener la IP del servidor:**
   ```powershell
   ipconfig
   ```

2. **Desde otro computador o telefono, consumir la API:**
   ```powershell
   Invoke-RestMethod -Method GET -Uri http://<IP_DEL_SERVIDOR>:3000/tasks `
     -Headers @{Authorization="Bearer $token"}
   ```

3. **Resultado:** Conexion exitosa. La API responde correctamente desde dispositivos remotos en la misma red.

## Estructura del Proyecto

```
Lab 2/
├── server.js           # Servidor principal con todos los endpoints implementados
├── server-solucion.js  # Solucion de referencia (solo para el profesor)
├── decodificar.js      # Script para decodificar y analizar tokens JWT
└── README.md           # Documentacion del laboratorio
```

## Como Ejecutar

1. **Iniciar el servidor:**
   ```bash
   node server.js
   ```

2. **El servidor estara disponible en:**
   - Local: `http://localhost:3000`
   - Remoto: `http://<TU_IP>:3000`

3. **Ejecutar pruebas con PowerShell** (segunda terminal):
   ```powershell
   # Registro
   Invoke-RestMethod -Method POST -Uri http://localhost:3000/auth/register `
     -ContentType "application/json" `
     -Body '{"username":"test","email":"test@test.com","password":"1234"}'

   # Login
   $token = (Invoke-RestMethod -Method POST -Uri http://localhost:3000/auth/login `
     -ContentType "application/json" `
     -Body '{"email":"test@test.com","password":"1234"}').token

   # Crear tarea
   $tarea = Invoke-RestMethod -Method POST -Uri http://localhost:3000/tasks `
     -ContentType "application/json" `
     -Headers @{Authorization="Bearer $token"} `
     -Body '{"title":"Mi tarea","description":"Descripcion"}'

   # Actualizar tarea (PUT)
   Invoke-RestMethod -Method PUT -Uri http://localhost:3000/tasks/$($tarea.id) `
     -ContentType "application/json" `
     -Headers @{Authorization="Bearer $token"} `
     -Body '{"status":"completed"}'

   # Eliminar tarea (DELETE)
   Invoke-RestMethod -Method DELETE -Uri http://localhost:3000/tasks/$($tarea.id) `
     -Headers @{Authorization="Bearer $token"}
   ```

## Seguridad

- **JWT emulado:** Implementado con HMAC-SHA256 para firmar tokens
- **Expiracion:** Los tokens expiran en 1 hora (3600000 ms)
- **Autorizacion:** Cada endpoint protegido verifica que el usuario sea el dueño del recurso
- **Códigos de error apropiados:**
  - `401` - No autenticado o token invalido
  - `403` - Sin permisos para el recurso
  - `404` - Recurso no encontrado

## Autor
Laboratorio desarrollado para la asignatura de Ingenieria de Software II - Semestre 2026-1
