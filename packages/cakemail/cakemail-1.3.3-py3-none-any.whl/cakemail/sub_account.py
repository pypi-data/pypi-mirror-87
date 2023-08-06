from cakemail_openapi import SubAccountApi
from cakemail.wrapper import WrappedApi


class SubAccount(WrappedApi):
    confirm: SubAccountApi.confirm_account
    create: SubAccountApi.create_account
    delete: SubAccountApi.delete_account
    get: SubAccountApi.get_account
    list: SubAccountApi.list_accounts
    update: SubAccountApi.patch_account
    resend_verification: SubAccountApi.resend_account_verification
    suspend: SubAccountApi.suspend_account
    unsuspend: SubAccountApi.unsuspend_account

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'confirm': 'confirm_account',
                'create': 'create_account',
                'delete': 'delete_account',
                'get': 'get_account',
                'list': 'list_accounts',
                'update': 'patch_account',
                'resend_verification': 'resend_account_verification',
                'suspend': 'suspend_account',
                'unsuspend': 'unsuspend_account',
            }
        )
