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


class NotificationSystemFacade:
    def __init__(self):
        self._bus = EventBus()
        self._builder = MessageBuilder()
        self._dispatcher = NotificationDispatcher()
        self._dispatcher.add_sender(EmailAdapter(EmailService()))
        self._dispatcher.add_sender(SMSAdapter(SMSService()))
        self._dispatcher.add_sender(PushAdapter(PushService()))
        self._templates = {}

    def register_template(self, name, template):
        self._templates[name] = template
        print(f"  [FACADE] Plantilla registrada: '{name}' -> {template}")

    def create_from_template(self, template_name, recipient, **customizations):
        base = self._templates.get(template_name)
        if base is None:
            raise ValueError(f"Plantilla no encontrada: {template_name}")
        customized = base.customize(**customizations)
        msg = (
            self._builder.set_recipient(recipient)
            .set_subject(customized.subject)
            .set_body(customized.body)
            .set_priority(customized.priority)
            .build()
        )
        return msg

    def create_notification(self, notification_type, recipient, content):
        return NotificationFactory.create(notification_type, recipient, content)

    def send_managed(self, notification):
        managed = ManagedNotification(notification)
        print(f"  [FACADE] Estado inicial: {managed}")
        managed.send(self._dispatcher)
        print(f"  [FACADE] Estado tras envío: {managed}")
        self._bus.publish("notificacion_enviada", notification)
        return managed

    def send_simple(self, recipient, subject, body, priority="normal"):
        msg = (
            self._builder.set_recipient(recipient)
            .set_subject(subject)
            .set_body(body)
            .set_priority(priority)
            .build()
        )
        self._dispatcher.dispatch(msg)
        self._bus.publish("mensaje_enviado", msg)
        return msg

    def get_bus(self):
        return self._bus
