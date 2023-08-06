from cakemail_openapi import ListApi
from cakemail.wrapper import WrappedApi


class List(WrappedApi):
    accept_policy: ListApi.accept_list_policy
    archive: ListApi.archive_list
    create: ListApi.create_list
    delete: ListApi.delete_list
    get: ListApi.get_list
    list: ListApi.list_lists
    update: ListApi.patch_list
    unarchive: ListApi.unarchive_list

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'accept_policy': 'accept_list_policy',
                'archive': 'archive_list',
                'create': 'create_list',
                'delete': 'delete_list',
                'get': 'get_list',
                'list': 'list_lists',
                'update': 'patch_list',
                'unarchive': 'unarchive_list',
            }
        )
