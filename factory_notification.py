from abc import ABC, abstractmethod


class Notification(ABC):
    def __init__(self, recipient, content):
        self.recipient = recipient
        self.content = content
        self.subject = self.get_type()
        self.body = content
        self.priority = "normal"
        self.attachments = []

    @abstractmethod
    def get_type(self) -> str:
        pass

    def __str__(self):
        return f"[{self.get_type()}] -> {self.recipient}: {self.content}"


class AlertNotification(Notification):
    def get_type(self):
        return "ALERTA"


class ReminderNotification(Notification):
    def get_type(self):
        return "RECORDATORIO"


class PromotionalNotification(Notification):
    def get_type(self):
        return "PROMOCIÓN"


class NotificationFactory:
    _creators = {
        "alerta": AlertNotification,
        "recordatorio": ReminderNotification,
        "promocion": PromotionalNotification,
    }

    @classmethod
    def create(cls, notification_type, recipient, content):
        creator = cls._creators.get(notification_type.lower())
        if creator is None:
            raise ValueError(f"Tipo de notificación desconocido: {notification_type}")
        return creator(recipient, content)
