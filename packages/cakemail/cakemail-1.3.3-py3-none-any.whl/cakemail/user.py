from cakemail_openapi import UserApi
from cakemail.wrapper import WrappedApi


class User(WrappedApi):
    confirm: UserApi.confirm_user
    create: UserApi.create_user
    delete: UserApi.delete_user
    forgot_my_password: UserApi.forgot_my_password
    get_self: UserApi.get_self_user
    get: UserApi.get_user
    list: UserApi.list_users
    update: UserApi.patch_user
    resend_verification: UserApi.resend_user_verification
    reset_password_confirm: UserApi.reset_password_confirm
    reset_self_password: UserApi.reset_self_password
    reset_password: UserApi.reset_user_password
    suspend: UserApi.suspend_user
    unsuspend: UserApi.unsuspend_user

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'confirm': 'confirm_user',
                'create': 'create_user',
                'delete': 'delete_user',
                'forgot_my_password': 'forgot_my_password',
                'get_self': 'get_self_user',
                'get': 'get_user',
                'list': 'list_users',
                'update': 'patch_user',
                'resend_verification': 'resend_user_verification',
                'reset_password_confirm': 'reset_password_confirm',
                'reset_self_password': 'reset_self_password',
                'reset_password': 'reset_user_password',
                'suspend': 'suspend_user',
                'unsuspend': 'unsuspend_user',
            }
        )
