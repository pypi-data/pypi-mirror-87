from cakemail_openapi import FormApi
from cakemail.wrapper import WrappedApi


class Form(WrappedApi):
    create: FormApi.create_form
    delete: FormApi.delete_form
    get: FormApi.get_form
    list: FormApi.list_forms
    update: FormApi.patch_form

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_form',
                'delete': 'delete_form',
                'get': 'get_form',
                'list': 'list_forms',
                'update': 'patch_form',
            }
        )
