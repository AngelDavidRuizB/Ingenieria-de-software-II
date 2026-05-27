from abc import ABC, abstractmethod


class NotificationState(ABC):
    @abstractmethod
    def send(self, notification, dispatcher) -> "NotificationState":
        pass

    @abstractmethod
    def cancel(self, notification) -> "NotificationState":
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class DraftState(NotificationState):
    def send(self, notification, dispatcher):
        print(f"  [ESTADO] Borrador enviado: {notification}")
        dispatcher.dispatch(notification)
        return PendingState()

    def cancel(self, notification):
        print(f"  [ESTADO] Borrador cancelado: {notification}")
        return CancelledState()

    def get_name(self):
        return "BORRADOR"


class PendingState(NotificationState):
    def send(self, notification, dispatcher):
        print(f"  [ESTADO] Ya fue enviada, no se puede reenviar: {notification}")
        return self

    def cancel(self, notification):
        print(f"  [ESTADO] Envío cancelado: {notification}")
        return CancelledState()

    def get_name(self):
        return "PENDIENTE"


class SentState(NotificationState):
    def send(self, notification, dispatcher):
        print(f"  [ESTADO] Ya fue entregada: {notification}")
        return self

    def cancel(self, notification):
        print(f"  [ESTADO] No se puede cancelar una notificación entregada: {notification}")
        return self

    def get_name(self):
        return "ENTREGADA"


class CancelledState(NotificationState):
    def send(self, notification, dispatcher):
        print(f"  [ESTADO] Notificación cancelada, no se puede enviar: {notification}")
        return self

    def cancel(self, notification):
        print(f"  [ESTADO] Ya estaba cancelada: {notification}")
        return self

    def get_name(self):
        return "CANCELADA"


class ManagedNotification:
    def __init__(self, notification):
        self.notification = notification
        self._state = DraftState()

    @property
    def state_name(self):
        return self._state.get_name()

    def send(self, dispatcher):
        self._state = self._state.send(self.notification, dispatcher)

    def cancel(self):
        self._state = self._state.cancel(self.notification)

    def __str__(self):
        return f"[{self.state_name}] {self.notification}"
