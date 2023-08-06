"""
Main notifier class.
"""
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from traceback_notifier import settings
from traceback_notifier.custom_exceptions import ConfigurationError


class Notifier:
    """
    Class to send notification email with exception and traceback.
    """

    def __init__(self) -> None:
        self.validate_config()
        self.scope = settings.SCOPE
        self.email_from = settings.EMAIL_FROM
        self.sendgrid_client = self._setup_sendgrid()
        self.triggered = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    @staticmethod
    def validate_config() -> None:
        """
        Check that all config parameters are set.
        :return: None
        """
        if settings.SENDGRID_API_TOKEN is None:
            raise ConfigurationError("Sendgrid token is not set.")
        if settings.EMAIL_FROM is None:
            raise ConfigurationError("Email from is not set.")
        if not settings.SEND_TO:
            raise ConfigurationError("Send-to list is empty.")
        if not settings.SCOPE:
            raise ConfigurationError("Scope is not set.")

    @staticmethod
    def _setup_sendgrid() -> SendGridAPIClient:
        """
        Initiate sendgrid client.
        :return: Sendgrid api client instance.
        :rtype: SendGridAPIClient
        """
        client = SendGridAPIClient(settings.SENDGRID_API_TOKEN)
        return client

    def generate_subject(self, exception: Exception) -> str:
        """
        Generate email subject
        :param exception: Exception instance
        :return: string with scope, exception name and time triggered.
        """
        return f"{self.scope}: {exception.__class__.__name__} | {self.triggered}"

    def render_html(self, exception: Exception, traceback: str) -> str:
        """
        Renders jinja template.
        :param exception: raised Exception.
        :param traceback: formatted traceback of exception.
        :return: string with html markup to send via email
        """
        env = Environment(
            loader=FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('traceback.html')
        html = template.render(**dict(exception_name=exception.__class__.__name__,
                                      timestamp=self.triggered,
                                      traceback=traceback,
                                      scope=self.scope))
        return html

    def notify(self, exception: Exception, traceback: str) -> None:
        """
        Send email with traceback info.
        :param exception: raised Exception.
        :param traceback: formatted traceback of exception.
        :return: None
        """
        mail = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=settings.SEND_TO,
            subject=self.generate_subject(exception),
            html_content=self.render_html(exception, traceback)
        )
        self.sendgrid_client.send(mail)
