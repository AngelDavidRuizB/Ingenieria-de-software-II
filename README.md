# Sistema de Notificaciones Multi-Canal — Patrones de Diseño GoF en Python

Proyecto académico para la asignatura **Ingeniería de Software II** que implementa **7 patrones de diseño del GoF** integrados en un sistema de notificaciones multi-canal. El objetivo es demostrar cómo los patrones de las tres categorías (creacionales, estructurales y de comportamiento) pueden combinarse en una solución coherente y funcional.

---

## Requisitos

- Python 3.8 o superior
- No se requieren dependencias externas (solo librería estándar)

## Ejecución

```bash
python main.py
```

---

## Patrones implementados

### Creacionales (4)

| Patrón | Archivo | Clase(s) principal(es) | Propósito |
|---|---|---|---|
| **Singleton** | `singleton_event_bus.py` | `EventBus` | Garantiza una única instancia global del bus de eventos del sistema |
| **Factory Method** | `factory_notification.py` | `NotificationFactory`, `Notification`, `AlertNotification`, `ReminderNotification`, `PromotionalNotification` | Encapsula la creación de notificaciones por tipo sin acoplar al cliente con clases concretas |
| **Prototype** | `prototype_template.py` | `NotificationTemplate` | Permite clonar plantillas de notificación y personalizarlas sin reconstruirlas desde cero |
| **Builder** | `builder_message.py` | `Message`, `MessageBuilder` | Construye mensajes complejos paso a paso con interfaz fluida (method chaining) |

### Estructurales (2)

| Patrón | Archivo | Clase(s) principal(es) | Propósito |
|---|---|---|---|
| **Adapter** | `adapter_notification.py` | `NotificationSender`, `EmailAdapter`, `SMSAdapter`, `PushAdapter`, `NotificationDispatcher` | Unifica APIs incompatibles (Email, SMS, Push) bajo una interfaz común de envío |
| **Facade** | `facade_system.py` | `NotificationSystemFacade` | Ofrece una interfaz simplificada que integra todos los subsistemas del proyecto |

### De comportamiento (1)

| Patrón | Archivo | Clase(s) principal(es) | Propósito |
|---|---|---|---|
| **State** | `state_notification.py` | `NotificationState`, `DraftState`, `PendingState`, `SentState`, `CancelledState`, `ManagedNotification` | Modela el ciclo de vida de una notificación como máquina de estados con transiciones controladas |

---

## Estructura del proyecto

```
Patterns/
├── main.py                     # Punto de entrada — orquesta los 7 patrones en 8 secciones
├── singleton_event_bus.py      # Singleton — Bus de eventos global único
├── factory_notification.py     # Factory Method — Creación de notificaciones por tipo
├── prototype_template.py       # Prototype — Clonación de plantillas de notificación
├── builder_message.py          # Builder — Construcción paso a paso de mensajes
├── adapter_notification.py     # Adapter — Adaptadores para Email, SMS y Push
├── facade_system.py            # Facade — Interfaz unificada del sistema completo
├── state_notification.py       # State — Máquina de estados del ciclo de vida
├── Instrucciones base.md       # Documento original de la actividad
├── Instrucciones v2.md         # Documento de instrucciones de esta versión
└── README.md                   # Este archivo
```

---

## Flujo de ejecución

El `main.py` ejecuta 8 secciones secuenciales que demuestran cada patrón:

```
1. Verificación Singleton
   └─ Confirma que EventBus es una instancia única

2. Factory Method
   └─ Crea 3 notificaciones: alerta, recordatorio, promoción

3. Prototype
   └─ Clona una plantilla base y la personaliza con atributos distintos

4. Builder
   └─ Construye 2 mensajes complejos con method chaining

5. Adapter
   └─ Envía un mensaje por 3 canales: Email, SMS, Push

6. State
   └─ Demuestra transiciones: borrador→cancelada, borrador→pendiente, reenvío rechazado

7. Facade
   └─ Usa la interfaz simplificada: registro de plantillas, creación, envío gestionado y simple

8. Verificación final
   └─ Confirma que el Facade usa el mismo Singleton
```

---

## Diagrama de interacción entre patrones

```
                    ┌─────────────────────────┐
                    │   NotificationSystem    │
                    │       Facade            │
                    └────────┬────────────────┘
                             │ integra
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
   ┌─────────────┐  ┌──────────────┐  ┌────────────────┐
   │ EventBus    │  │ Message      │  │ Notification   │
   │ Singleton   │  │ Builder      │  │ Factory        │
   └─────────────┘  └──────────────┘  └────────────────┘
                             │                  │
                             ▼                  ▼
                    ┌──────────────┐  ┌────────────────┐
                    │ Notification │  │ Notification   │
                    │ Dispatcher   │  │ Template       │
                    │  ┌─────────┐ │  │ Prototype      │
                    │  │Adapter  │ │  └────────────────┘
                    │  │Email    │ │
                    │  │SMS      │ │
                    │  │Push     │ │
                    │  └─────────┘ │
                    └──────┬───────┘
                           │ envía
                           ▼
                    ┌──────────────┐
                    │ Managed      │
                    │ Notification │
                    │   State      │
                    │ Borrador     │
                    │ Pendiente    │
                    │ Entregada    │
                    │ Cancelada    │
                    └──────────────┘
```

---

## Detalle de cada patrón

### Singleton — `EventBus`

Implementa el patrón mediante `__new__` para controlar la creación de instancias. El atributo `_subscribers` se inicializa solo la primera vez. Cualquier llamada posterior a `EventBus()` devuelve la misma instancia.

```python
bus_a = EventBus()
bus_b = EventBus()
assert bus_a is bus_b  # True
```

### Factory Method — `NotificationFactory`

Usa un diccionario de clases (`_creators`) para mapear strings a clases concretas. El método `create()` instancia la clase correspondiente sin que el cliente conozca las implementaciones.

```python
n = NotificationFactory.create("alerta", "admin@empresa.com", "Servidor caído")
# Devuelve una instancia de AlertNotification
```

### Prototype — `NotificationTemplate`

Utiliza `copy.deepcopy` para clonar objetos completos (incluyendo listas anidadas como `tags`). El método `customize()` devuelve un clon con los atributos modificados, dejando el original intacto.

```python
base = NotificationTemplate(subject="Aviso", body="...", priority="normal")
clone = base.customize(subject="URGENTE", priority="alta")
assert base is not clone  # True — objetos independientes
```

### Builder — `MessageBuilder`

Cada método `set_*` retorna `self`, permitiendo encadenar llamadas. El método `build()` devuelve el mensaje construido y reinicia el builder para reutilización.

```python
msg = (MessageBuilder()
       .set_recipient("user@mail.com")
       .set_subject("Hola")
       .set_body("Contenido")
       .set_priority("alta")
       .build())
```

### Adapter — `NotificationSender`

Tres servicios con APIs distintas (`send_email`, `send_sms`, `deliver_push`) se envuelven en adaptadores que implementan la interfaz común `NotificationSender.send()`. El `NotificationDispatcher` itera sobre todos los adaptadores sin conocer los detalles de cada canal.

```python
dispatcher = NotificationDispatcher()
dispatcher.add_sender(EmailAdapter(EmailService()))
dispatcher.add_sender(SMSAdapter(SMSService()))
dispatcher.dispatch(message)  # Envía por todos los canales
```

### Facade — `NotificationSystemFacade`

Compone internamente el Singleton, Builder, Factory, Prototype y Adapter en una sola clase. El cliente interactúa con métodos de alto nivel sin conocer los subsistemas.

```python
facade = NotificationSystemFacade()
facade.register_template("bienvenida", template)
msg = facade.create_from_template("bienvenida", "user@mail.com")
facade.send_managed(notification)
```

### State — `ManagedNotification`

Modela 4 estados (`BORRADOR`, `PENDIENTE`, `ENTREGADA`, `CANCELADA`) con transiciones controladas:

```
BORRADOR ──enviar──→ PENDIENTE
BORRADOR ──cancelar─→ CANCELADA
PENDIENTE ──cancelar─→ CANCELADA
```

Cualquier otra transición es rechazada sin cambiar el estado.

```python
managed = ManagedNotification(notification)
managed.send(dispatcher)   # BORRADOR → PENDIENTE
managed.send(dispatcher)   # Rechazado: "Ya fue enviada"
```

---

## Combinación Singleton + otros patrones

El requisito de combinar Singleton con al menos otro patrón se cumple en `facade_system.py`:

- El `NotificationSystemFacade` obtiene la instancia única de `EventBus` (Singleton).
- Publica eventos en ese bus al enviar notificaciones.
- También combina internamente Builder, Factory, Prototype, Adapter y State.

Esto garantiza que todo el sistema comparta el mismo bus de eventos sin necesidad de pasarlo explícitamente entre componentes.

---

## Cobertura de categorías GoF

| Categoría | Patrones | Archivos |
|---|---|---|
| **Creacional** | Singleton, Factory Method, Prototype, Builder | `singleton_event_bus.py`, `factory_notification.py`, `prototype_template.py`, `builder_message.py` |
| **Estructural** | Adapter, Facade | `adapter_notification.py`, `facade_system.py` |
| **Comportamiento** | State | `state_notification.py` |
