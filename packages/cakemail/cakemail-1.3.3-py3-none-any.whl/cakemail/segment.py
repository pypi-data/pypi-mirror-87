from cakemail_openapi import SegmentApi
from cakemail.wrapper import WrappedApi


class Segment(WrappedApi):
    create: SegmentApi.create_segment
    delete: SegmentApi.delete_segment
    get: SegmentApi.get_segment
    list: SegmentApi.list_segments
    update: SegmentApi.patch_segment

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_segment',
                'delete': 'delete_segment',
                'get': 'get_segment',
                'list': 'list_segments',
                'update': 'patch_segment',
            }
        )
