from cakemail_openapi import AccountApi
from cakemail.wrapper import WrappedApi


class Account(WrappedApi):
    get_self: AccountApi.get_self_account
    update_self: AccountApi.patch_self_account

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'get_self': 'get_self_account',
                'update_self': 'patch_self_account',
            }
        )
