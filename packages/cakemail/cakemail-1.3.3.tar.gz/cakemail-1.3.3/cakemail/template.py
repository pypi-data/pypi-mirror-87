from cakemail_openapi import TemplateApi
from cakemail.wrapper import WrappedApi


class Template(WrappedApi):
    create: TemplateApi.create_template
    delete: TemplateApi.delete_template
    get: TemplateApi.get_template
    list: TemplateApi.list_templates
    update: TemplateApi.patch_template

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_template',
                'delete': 'delete_template',
                'get': 'get_template',
                'list': 'list_templates',
                'update': 'patch_template',
            }
        )
