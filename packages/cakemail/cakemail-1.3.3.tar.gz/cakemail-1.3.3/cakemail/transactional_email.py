from cakemail_openapi import TransactionalEmailApi
from cakemail.wrapper import WrappedApi


class TransactionalEmail(WrappedApi):
    send: TransactionalEmailApi.send_email

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'send': 'send_email',
            }
        )
