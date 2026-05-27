class Message:
    def __init__(self):
        self.subject = ""
        self.body = ""
        self.recipient = ""
        self.priority = "normal"
        self.attachments = []

    def __str__(self):
        return (
            f"[{self.priority.upper()}] Para: {self.recipient} | "
            f"Asunto: {self.subject} | Cuerpo: {self.body} | "
            f"Adjuntos: {len(self.attachments)}"
        )


class MessageBuilder:
    def __init__(self):
        self._message = Message()

    def set_subject(self, subject):
        self._message.subject = subject
        return self

    def set_body(self, body):
        self._message.body = body
        return self

    def set_recipient(self, recipient):
        self._message.recipient = recipient
        return self

    def set_priority(self, priority):
        self._message.priority = priority
        return self

    def add_attachment(self, attachment):
        self._message.attachments.append(attachment)
        return self

    def build(self):
        result = self._message
        self._message = Message()
        return result
