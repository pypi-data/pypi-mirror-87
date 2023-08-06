from cakemail_openapi import ContactApi
from cakemail.wrapper import WrappedApi


class Contact(WrappedApi):
    create: ContactApi.create_contact
    delete: ContactApi.delete_contact
    get: ContactApi.get_contact
    import_contacts: ContactApi.import_contacts
    list: ContactApi.list_contacts_of_list
    list_from_segments: ContactApi.list_contacts_of_segment
    update: ContactApi.patch_contact
    unsubscribe: ContactApi.unsubscribe_contact

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_contact',
                'delete': 'delete_contact',
                'get': 'get_contact',
                'import_contacts': 'import_contacts',
                'list': 'list_contacts_of_list',
                'list_from_segments': 'list_contacts_of_segment',
                'update': 'patch_contact',
                'unsubscribe': 'unsubscribe_contact',
            }
        )
