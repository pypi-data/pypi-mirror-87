from cakemail_openapi import DomainApi
from cakemail.wrapper import WrappedApi


class Domain(WrappedApi):
    update: DomainApi.patch_domains
    show: DomainApi.show_domains
    validate: DomainApi.validate_domains

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'update': 'patch_domains',
                'show': 'show_domains',
                'validate': 'validate_domains',
            }
        )
