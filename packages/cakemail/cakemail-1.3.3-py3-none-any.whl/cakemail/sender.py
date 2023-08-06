from cakemail_openapi import SenderApi
from cakemail.wrapper import WrappedApi


class Sender(WrappedApi):
    confirm: SenderApi.confirm_sender
    create: SenderApi.create_sender
    delete: SenderApi.delete_sender
    get: SenderApi.get_sender
    list: SenderApi.list_senders
    update: SenderApi.patch_sender
    resend_confirmation: SenderApi.resend_confirmation_email

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'confirm': 'confirm_sender',
                'create': 'create_sender',
                'delete': 'delete_sender',
                'get': 'get_sender',
                'list': 'list_senders',
                'update': 'patch_sender',
                'resend_confirmation': 'resend_confirmation_email',
            }
        )
