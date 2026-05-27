from singleton_event_bus import EventBus
from builder_message import MessageBuilder
from factory_notification import NotificationFactory
from prototype_template import NotificationTemplate
from adapter_notification import (
    EmailService,
    SMSService,
    PushService,
    EmailAdapter,
    SMSAdapter,
    PushAdapter,
    NotificationDispatcher,
)
from state_notification import ManagedNotification
from facade_system import NotificationSystemFacade


def main():
    print("=" * 60)
    print("SISTEMA DE NOTIFICACIONES - PATRONES DE DISEÑO")
    print("=" * 60)

    print("\n--- 1. Verificación Singleton ---")
    bus_a = EventBus()
    bus_b = EventBus()
    print(f"EventBus único (singleton): {bus_a is bus_b}")

    print("\n--- 2. Factory Method: creación de notificaciones ---")
    n1 = NotificationFactory.create("alerta", "admin@empresa.com", "Servidor caído")
    n2 = NotificationFactory.create("recordatorio", "usuario@mail.com", "Reunión a las 3PM")
    n3 = NotificationFactory.create("promocion", "cliente@tienda.com", "50% de descuento")
    print(f"  {n1}")
    print(f"  {n2}")
    print(f"  {n3}")

    print("\n--- 3. Prototype: clonación y personalización de plantillas ---")
    base_template = NotificationTemplate(
        subject="Aviso del sistema",
        body="Estimado usuario, le informamos que...",
        priority="normal",
        tags=["sistema", "automático"],
    )
    print(f"  Plantilla base: {base_template}")

    critical_clone = base_template.customize(
        subject="ALERTA CRÍTICA",
        priority="alta",
        tags=["sistema", "urgente"],
    )
    print(f"  Clon personalizado: {critical_clone}")
    print(f"  ¿Son objetos distintos? {base_template is not critical_clone}")

    print("\n--- 4. Builder: construcción paso a paso de mensajes ---")
    builder = MessageBuilder()
    msg1 = (
        builder.set_recipient("admin@empresa.com")
        .set_subject("Alerta de seguridad")
        .set_body("Se detectó un inicio de sesión inusual.")
        .set_priority("alta")
        .build()
    )
    print(f"  Mensaje 1: {msg1}")

    msg2 = (
        builder.set_recipient("+573001234567")
        .set_subject("Recordatorio")
        .set_body("Tu cita es mañana a las 10:00 AM.")
        .set_priority("normal")
        .add_attachment("cita.pdf")
        .build()
    )
    print(f"  Mensaje 2: {msg2}")

    print("\n--- 5. Adapter: envío multi-canal ---")
    dispatcher = NotificationDispatcher()
    dispatcher.add_sender(EmailAdapter(EmailService()))
    dispatcher.add_sender(SMSAdapter(SMSService()))
    dispatcher.add_sender(PushAdapter(PushService()))

    print("  Enviando mensaje 1 por todos los canales:")
    dispatcher.dispatch(msg1)

    print("\n--- 6. State: ciclo de vida de notificaciones ---")
    managed = ManagedNotification(n1)
    print(f"  Estado inicial: {managed}")

    print("  Intentando cancelar el borrador:")
    managed.cancel()
    print(f"  Estado tras cancelar: {managed}")

    managed2 = ManagedNotification(n2)
    print(f"\n  Nueva notificación: {managed2}")
    print("  Enviando notificación:")
    managed2.send(dispatcher)
    print(f"  Estado tras envío: {managed2}")

    print("  Intentando reenviar:")
    managed2.send(dispatcher)

    print("\n--- 7. Facade: uso simplificado del sistema ---")
    facade = NotificationSystemFacade()

    facade.register_template("bienvenida", NotificationTemplate(
        subject="Bienvenido a la plataforma",
        body="Gracias por registrarte.",
        priority="normal",
        tags=["onboarding"],
    ))
    facade.register_template("alerta_seguridad", NotificationTemplate(
        subject="Actividad sospechosa detectada",
        body="Se detectó un acceso desde una ubicación desconocida.",
        priority="alta",
        tags=["seguridad"],
    ))

    print("\n  Creando mensaje desde plantilla 'bienvenida':")
    welcome_msg = facade.create_from_template("bienvenida", "nuevo@usuario.com")
    print(f"  {welcome_msg}")

    print("\n  Enviando notificación gestionada vía Facade:")
    alert_notif = facade.create_notification("alerta", "admin@empresa.com", "Disco lleno")
    facade.send_managed(alert_notif)

    print("\n  Envío simple vía Facade:")
    facade.send_simple(
        recipient="equipo@empresa.com",
        subject="Despliegue completado",
        body="La versión 2.1 fue desplegada exitosamente.",
        priority="normal",
    )

    print("\n--- 8. Verificación final del Singleton ---")
    bus_from_facade = facade.get_bus()
    print(f"  ¿El bus del Facade es el mismo Singleton? {bus_from_facade is bus_a}")

    print("\n" + "=" * 60)
    print("EJECUCIÓN COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    main()
