# Ejercicio de patrones de diseño en Python — Versión 2

## Descripción extensa de la actividad

La actividad pide construir un ejemplo práctico en Python donde:

1. Se use el patrón `Singleton`.
2. Ese patrón se combine con otro patrón adicional.
3. Se intente cubrir los tres grandes grupos de patrones GOF:
   - Creacionales.
   - Estructurales.
   - De comportamiento.
4. Además, dentro de lo creacional no quedarse solo con Singleton, sino incluir otros patrones de la misma categoría.

La solución se diseñó como un **sistema de notificaciones multi-canal** para que la integración sea realista:

- Primero se crean notificaciones y mensajes mediante distintos mecanismos creacionales.
- Luego se adaptan los canales de envío y se simplifica el acceso al sistema (estructurales).
- Finalmente se gestiona el ciclo de vida de cada notificación (comportamiento).

## Patrones implementados y rol de cada uno

### 1) Creacionales

- **Singleton** en `singleton_event_bus.py`
  - Clase principal: `EventBus`.
  - Objetivo: garantizar un único bus de eventos global donde se publican y suscriben todos los eventos del sistema.
  - Validación conceptual: dos variables distintas (`bus_a`, `bus_b`) apuntan al mismo objeto.

- **Factory Method** en `factory_notification.py`
  - Clases principales: `NotificationFactory`, `Notification` (abstracta), `AlertNotification`, `ReminderNotification`, `PromotionalNotification`.
  - Objetivo: encapsular la creación de distintos tipos de notificación sin que el cliente conozca las clases concretas. Se invoca con un string (`"alerta"`, `"recordatorio"`, `"promocion"`) y devuelve el objeto adecuado.

- **Prototype** en `prototype_template.py`
  - Clases principales: `NotificationTemplate`.
  - Objetivo: permitir la clonación profunda de plantillas de notificación predefinidas, personalizando atributos sin reconstruir el objeto desde cero. Se usa `copy.deepcopy` para garantizar independencia entre original y clon.

- **Builder** en `builder_message.py`
  - Clases principales: `Message`, `MessageBuilder`.
  - Objetivo: construir mensajes complejos paso a paso (destinatario, asunto, cuerpo, prioridad, adjuntos) mediante una interfaz fluida (method chaining).

### 2) Estructurales

- **Adapter** en `adapter_notification.py`
  - Clases principales: `NotificationSender` (interfaz común), `EmailAdapter`, `SMSAdapter`, `PushAdapter`.
  - Servicios adaptados: `EmailService`, `SMSService`, `PushService`.
  - Objetivo: unificar la interfaz de envío para que servicios con APIs incompatibles (email, SMS, push) puedan usarse de manera intercambiable a través de un `NotificationDispatcher`.

- **Facade** en `facade_system.py`
  - Clase principal: `NotificationSystemFacade`.
  - Objetivo: ofrecer una interfaz simplificada que integra internamente el EventBus (Singleton), el MessageBuilder, el NotificationFactory, el Prototype y el NotificationDispatcher (Adapter). El cliente usa un solo objeto para registrar plantillas, crear mensajes, enviar notificaciones gestionadas y envíos simples.

### 3) De comportamiento

- **State** en `state_notification.py`
  - Clases principales: `NotificationState` (abstracta), `DraftState`, `PendingState`, `SentState`, `CancelledState`, `ManagedNotification`.
  - Objetivo: modelar el ciclo de vida de una notificación como una máquina de estados. Cada estado define qué ocurre al intentar enviar o cancelar, y devuelve el nuevo estado resultante. Las transiciones válidas son:
    - `BORRADOR` → `PENDIENTE` (al enviar)
    - `BORRADOR` → `CANCELADA` (al cancelar)
    - `PENDIENTE` → `CANCELADA` (al cancelar)
    - Otros intentos son rechazados sin cambio de estado.

## Combinación solicitada: Singleton + otros patrones

La combinación se implementa en `facade_system.py`:

- `NotificationSystemFacade` (Facade) internamente obtiene la instancia única de `EventBus` (Singleton) y la usa para publicar eventos.
- También compone internamente un `MessageBuilder` (Builder), un `NotificationDispatcher` con adaptadores (Adapter) y gestiona notificaciones con ciclo de vida (State).
- Como el `EventBus` es `Singleton`, toda la comunicación por eventos del sistema pasa por la misma instancia compartida, sin importar desde dónde se invoque.

Con esto se cumple explícitamente la parte de "combinar Singleton con otro patrón".

## Orquestación completa del ejercicio

El archivo `main.py` integra todo el flujo en 8 secciones:

1. **Verificación Singleton**: comprueba que `EventBus` es único.
2. **Factory Method**: crea tres tipos distintos de notificación (alerta, recordatorio, promoción).
3. **Prototype**: clona una plantilla base y la personaliza con atributos diferentes.
4. **Builder**: construye dos mensajes complejos paso a paso.
5. **Adapter**: envía un mensaje por tres canales distintos (email, SMS, push).
6. **State**: demuestra el ciclo de vida de notificaciones (cancelar un borrador, enviar otra, intentar reenvío).
7. **Facade**: uso simplificado del sistema completo (registro de plantillas, creación desde plantilla, envío gestionado, envío simple).
8. **Verificación final**: confirma que el bus usado por el Facade es el mismo Singleton.

## Cómo se comprueba (paso a paso)

En Windows, ejecutar desde la carpeta del proyecto:

```bash
python main.py
```

Verificaciones esperadas en la salida:

1. `EventBus único (singleton): True`
   - Prueba directa de instancia única.

2. Tres notificaciones de tipos distintos creadas por Factory:
   - `[ALERTA]`, `[RECORDATORIO]`, `[PROMOCIÓN]`
   - Evidencia de creación encapsulada sin acoplamiento a clases concretas.

3. Clonación de plantilla con Prototype:
   - `¿Son objetos distintos? True`
   - Evidencia de independencia entre original y clon.

4. Dos mensajes construidos con Builder:
   - Con prioridad alta y sin adjuntos.
   - Con prioridad normal y un adjunto.

5. Tres canales de envío en Adapter:
   - `[EMAIL]`, `[SMS]`, `[PUSH]`
   - Evidencia de unificación de interfaces incompatibles.

6. Transiciones de State:
   - Borrador cancelado → `CANCELADA`.
   - Borrador enviado → `PENDIENTE`.
   - Reenvío rechazado: `Ya fue enviada, no se puede reenviar`.

7. Facade simplificando el uso:
   - Registro de plantillas, creación desde plantilla, envío gestionado y envío simple, todo con una sola interfaz.

8. `¿El bus del Facade es el mismo Singleton? True`
   - Confirmación de que el Facade usa la misma instancia global.

## Por qué sí es posible usar los tres tipos en este caso

Sí es posible porque el problema fue modelado en etapas con responsabilidades separadas:

1. **Creación de objetos** (`Singleton` + `Factory Method` + `Prototype` + `Builder`): múltiples mecanismos para distintos escenarios de construcción.
2. **Composición e integración** (`Adapter` + `Facade`): adaptación de interfaces incompatibles y simplificación del acceso al sistema.
3. **Gestión del comportamiento** (`State`): modelado del ciclo de vida de las notificaciones.

Estas etapas son compatibles entre sí y no se excluyen. El `EventBus` (Singleton) actúa como columna vertebral, el `Facade` orquesta todos los componentes, y cada patrón resuelve una preocupación específica sin interferir con los demás.

## Resumen final de cumplimiento

Se cumple todo lo solicitado:

1. `Singleton` implementado y comprobado (`EventBus`).
2. `Singleton` combinado con `Facade` (y también con `Adapter` y `State`).
3. Tres categorías cubiertas:
   - Creacional: `Singleton` + `Factory Method` + `Prototype` + `Builder`.
   - Estructural: `Adapter` + `Facade`.
   - Comportamiento: `State`.
