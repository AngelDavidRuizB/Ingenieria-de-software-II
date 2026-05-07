// decodificar.js — Ejercicio Fase 3
// Uso: node decodificar.js
//
// Instrucciones:
// 1. Correr el servidor: node server.js
// 2. Hacer login y copiar el token que retorna
// 3. Pegar el token en la variable TOKEN de abajo
// 4. Correr: node decodificar.js

const TOKEN = 'PEGAR_TOKEN_AQUI';

// -----------------------------------------------
// Decodificar sin verificar firma
// -----------------------------------------------
const partes = TOKEN.split('.');

if (partes.length !== 3) {
  console.log('Error: el token no tiene el formato correcto (header.payload.firma)');
  process.exit(1);
}

const [header, cuerpo, firma] = partes;

console.log('\n=== ESTRUCTURA DEL JWT ===\n');

console.log('--- HEADER (parte 1) ---');
const headerDecoded = JSON.parse(Buffer.from(header, 'base64').toString('utf8'));
console.log(headerDecoded);
console.log('Pregunta: que algoritmo se usa y que tipo de token es?\n');

console.log('--- PAYLOAD (parte 2) ---');
const payloadDecoded = JSON.parse(Buffer.from(cuerpo, 'base64').toString('utf8'));
console.log(payloadDecoded);
console.log('Pregunta: que datos viajan aqui? son privados o publicos?\n');

console.log('--- FIRMA (parte 3) ---');
console.log(firma);
console.log('Pregunta: si cambias una letra de esta firma, el servidor la aceptaria?\n');

// -----------------------------------------------
// Verificar expiracion
// -----------------------------------------------
const ahora = Date.now();
const expira = payloadDecoded.exp;
const minutosRestantes = Math.round((expira - ahora) / 60000);

console.log('=== ESTADO DEL TOKEN ===\n');
if (ahora > expira) {
  console.log('El token esta EXPIRADO');
} else {
  console.log(`El token es valido. Expira en aprox. ${minutosRestantes} minutos`);
}

// -----------------------------------------------
// Experimento: modificar el payload y verificar
// -----------------------------------------------
console.log('\n=== EXPERIMENTO: MANIPULACION ===\n');
const payloadFalso = { ...payloadDecoded, username: 'hacker', userId: '999' };
const cuerpoFalso  = Buffer.from(JSON.stringify(payloadFalso)).toString('base64').replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
const tokenManipulado = `${header}.${cuerpoFalso}.${firma}`;

console.log('Token original (primeros 40 chars):');
console.log(TOKEN.substring(0, 40) + '...');
console.log('\nToken manipulado (primeros 40 chars):');
console.log(tokenManipulado.substring(0, 40) + '...');
console.log('\nSon iguales?', TOKEN === tokenManipulado);
console.log('Conclusion: la firma del token manipulado ya NO coincide con la firma del servidor.');
console.log('El servidor rechazara este token aunque el payload parezca valido.');

// -----------------------------------------------
// Preguntas para responder en el cuaderno
// -----------------------------------------------
console.log('\n=== PREGUNTAS DEL LABORATORIO ===\n');
console.log('1. Que informacion viaja en el Header?');
console.log('2. Los datos del Payload estan cifrados o solo codificados en Base64?');
console.log('3. Por que NO se debe guardar la contrasena en el payload?');
console.log('4. Que pasa si alguien roba el token? Como se mitiga ese riesgo?');
console.log('5. Que diferencia hay entre Base64 (codificacion) y AES/RSA (cifrado)?');
