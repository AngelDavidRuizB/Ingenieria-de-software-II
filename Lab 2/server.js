// server.js — ToDo API sin dependencias externas
// Correr con: node server.js
// Requiere Node.js 14 o superior

const http   = require('http');
const crypto = require('crypto');

// -----------------------------------------------
// BASE DE DATOS EN MEMORIA
// -----------------------------------------------
const db = {
  users: [],
  tasks: []
};

// -----------------------------------------------
// JWT EMULADO — sin jsonwebtoken
// -----------------------------------------------
const SECRET = 'clave-secreta-laboratorio'; // En produccion: usar variable de entorno

function base64url(obj) {
  return Buffer.from(JSON.stringify(obj))
    .toString('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function firmar(datos) {
  return crypto
    .createHmac('sha256', SECRET)
    .update(datos)
    .digest('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function generarToken(payload) {
  const header = base64url({ alg: 'HS256', typ: 'JWT' });
  const cuerpo = base64url({ ...payload, exp: Date.now() + 3600000 });
  const firma  = firmar(`${header}.${cuerpo}`);
  return `${header}.${cuerpo}.${firma}`;
}

function verificarToken(token) {
  if (!token) return null;
  const partes = token.split('.');
  if (partes.length !== 3) return null;

  const [header, cuerpo, firma] = partes;
  const firmaEsperada = firmar(`${header}.${cuerpo}`);
  if (firma !== firmaEsperada) return null;

  const payload = JSON.parse(Buffer.from(cuerpo, 'base64').toString('utf8'));
  if (Date.now() > payload.exp) return null;

  return payload;
}

function autenticar(req) {
  const authHeader = req.headers['authorization'] || '';
  const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null;
  return verificarToken(token);
}

// -----------------------------------------------
// UTILIDADES HTTP
// -----------------------------------------------
function readBody(req) {
  return new Promise((resolve) => {
    let data = '';
    req.on('data', chunk => data += chunk);
    req.on('end', () => {
      try { resolve(JSON.parse(data)); }
      catch { resolve({}); }
    });
  });
}

function send(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body, null, 2));
}

// -----------------------------------------------
// SERVIDOR Y RUTAS
// -----------------------------------------------
const server = http.createServer(async (req, res) => {
  const url    = req.url;
  const method = req.method;

  // POST /auth/register
  if (method === 'POST' && url === '/auth/register') {
    const { username, email, password } = await readBody(req);

    if (!username || !email || !password)
      return send(res, 400, { error: 'Todos los campos son requeridos' });

    const existe = db.users.find(u => u.email === email);
    if (existe)
      return send(res, 409, { error: 'El email ya esta registrado' });

    const user = {
      id: Date.now().toString(),
      username,
      email,
      password
    };
    db.users.push(user);
    return send(res, 201, { message: 'Usuario creado', userId: user.id });
  }

  // POST /auth/login
  if (method === 'POST' && url === '/auth/login') {
    const { email, password } = await readBody(req);
    const user = db.users.find(u => u.email === email && u.password === password);

    if (!user)
      return send(res, 401, { error: 'Credenciales invalidas' });

    const token = generarToken({ userId: user.id, username: user.username });
    return send(res, 200, { token });
  }

  // GET /tasks
  if (method === 'GET' && url === '/tasks') {
    const usuario = autenticar(req);
    if (!usuario)
      return send(res, 401, { error: 'Token requerido o invalido' });

    const tareas = db.tasks.filter(t => t.userId === usuario.userId);
    return send(res, 200, { tasks: tareas });
  }

  // POST /tasks
  if (method === 'POST' && url === '/tasks') {
    const usuario = autenticar(req);
    if (!usuario)
      return send(res, 401, { error: 'Token requerido o invalido' });

    const { title, description } = await readBody(req);
    if (!title)
      return send(res, 400, { error: 'El titulo es requerido' });

    const task = {
      id: Date.now().toString(),
      title,
      description: description || '',
      status: 'pending',
      userId: usuario.userId,
      createdAt: new Date().toISOString()
    };
    db.tasks.push(task);
    return send(res, 201, task);
  }

  // PUT /tasks/:id
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

  // DELETE /tasks/:id
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

  send(res, 404, { error: 'Ruta no encontrada' });
});

server.listen(3000, '0.0.0.0', () => {
  console.log('Servidor corriendo en http://localhost:3000');
  console.log('Acceso remoto habilitado en 0.0.0.0:3000');
  console.log('Endpoints disponibles:');
  console.log('  POST /auth/register');
  console.log('  POST /auth/login');
  console.log('  GET  /tasks          (requiere token)');
  console.log('  POST /tasks          (requiere token)');
  console.log('  PUT  /tasks/:id      (requiere token)');
  console.log('  DELETE /tasks/:id    (requiere token)');
});
