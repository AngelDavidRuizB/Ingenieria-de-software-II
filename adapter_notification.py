from abc import ABC, abstractmethod


class NotificationSender(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailService:
    def send_email(self, to, subject, body):
        print(f"  [EMAIL] Enviando a {to}: '{subject}' - {body}")


class SMSService:
    def send_sms(self, phone, text):
        print(f"  [SMS] Enviando a {phone}: {text}")


class PushService:
    def deliver_push(self, device_token, payload):
        print(f"  [PUSH] Notificación a {device_token}: {payload}")


class EmailAdapter(NotificationSender):
    def __init__(self, service):
        self._service = service

    def send(self, message):
        self._service.send_email(message.recipient, message.subject, message.body)


class SMSAdapter(NotificationSender):
    def __init__(self, service):
        self._service = service

    def send(self, message):
        text = f"{message.subject}: {message.body}"
        self._service.send_sms(message.recipient, text)


class PushAdapter(NotificationSender):
    def __init__(self, service):
        self._service = service

    def send(self, message):
        payload = f"[{message.priority}] {message.subject}"
        self._service.deliver_push(message.recipient, payload)


class NotificationDispatcher:
    def __init__(self):
        self._senders = []

    def add_sender(self, sender):
        self._senders.append(sender)

    def dispatch(self, message):
        for sender in self._senders:
            sender.send(message)
