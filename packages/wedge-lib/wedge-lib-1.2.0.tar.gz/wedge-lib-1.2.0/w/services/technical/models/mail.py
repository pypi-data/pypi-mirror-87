from dataclasses import dataclass, field
from typing import Union, List

from django.conf import settings

from w.mixins.dataclasses_mixin import DataclassMixin

# todofsc: Use this or not on mail_service ?


@dataclass
class MailTemplate(DataclassMixin):
    template_name: str
    context: dict = None


@dataclass
class MailRecipients(DataclassMixin):
    to: Union[str, List[str]] = None
    bcc: Union[str, List[str]] = None
    cc: Union[str, List[str]] = None


@dataclass
class MailParams(DataclassMixin):
    subject: Union[str, MailTemplate]
    message: Union[str, MailTemplate]
    # if recipients is not a MailRecipients => recipients is 'to' recipient
    recipients: Union[str, list, MailRecipients]
    from_email: str = field(
        default_factory=lambda: settings.settings.DEFAULT_FROM_EMAIL
    )
    reply_to: str = field(default_factory=lambda: settings.settings.DEFAULT_REPLY_TO)
    attachments: list = field(default_factory=list)
    headers: dict = None
