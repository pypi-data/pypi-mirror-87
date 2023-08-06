from cakemail_openapi import SuppressedEmailApi
from cakemail.wrapper import WrappedApi


class SuppressedEmail(WrappedApi):
    create: SuppressedEmailApi.create_suppressed_email
    delete: SuppressedEmailApi.delete_suppressed_email
    list: SuppressedEmailApi.list_suppressed_emails

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_suppressed_email',
                'delete': 'delete_suppressed_email',
                'list': 'list_suppressed_emails',
            }
        )
