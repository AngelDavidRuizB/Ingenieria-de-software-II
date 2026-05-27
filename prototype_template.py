import copy


class NotificationTemplate:
    def __init__(self, subject, body, priority="normal", tags=None):
        self.subject = subject
        self.body = body
        self.priority = priority
        self.tags = tags if tags is not None else []

    def clone(self):
        return copy.deepcopy(self)

    def customize(self, **kwargs):
        cloned = self.clone()
        for key, value in kwargs.items():
            if hasattr(cloned, key):
                setattr(cloned, key, value)
        return cloned

    def __str__(self):
        return (
            f"Plantilla('{self.subject}' | prioridad={self.priority} | "
            f"tags={self.tags})"
        )
