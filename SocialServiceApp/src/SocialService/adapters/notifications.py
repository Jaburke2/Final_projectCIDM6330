import abc
import smtplib
from email.message import EmailMessage
from SocialService import config


class AbstractNotifications(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError


class EmailNotifications(AbstractNotifications):
    def __init__(self, smtp_host=None, port=None):
        self.smtp_host = smtp_host or config.get_email_host_and_port()["host"]
        self.port = port or config.get_email_host_and_port()["port"]

    def send(self, destination, message):
        msg = EmailMessage()
        msg["Subject"] = "Allocation Service Notification"
        msg["From"] = "allocations@example.com"
        msg["To"] = destination
        msg.set_content(message)

        with smtplib.SMTP(self.smtp_host, self.port) as smtp:
            smtp.send_message(msg)

