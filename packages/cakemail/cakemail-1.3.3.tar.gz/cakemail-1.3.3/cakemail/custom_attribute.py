from cakemail_openapi import CustomAttributeApi
from cakemail.wrapper import WrappedApi


class CustomAttribute(WrappedApi):
    create: CustomAttributeApi.create_custom_attribute
    delete: CustomAttributeApi.delete_custom_attribute
    get: CustomAttributeApi.get_custom_attribute
    list: CustomAttributeApi.list_custom_attributes

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_custom_attribute',
                'delete': 'delete_custom_attribute',
                'get': 'get_custom_attribute',
                'list': 'list_custom_attributes',
            }
        )
