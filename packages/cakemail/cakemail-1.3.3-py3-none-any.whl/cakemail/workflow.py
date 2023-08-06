from cakemail_openapi import WorkflowApi
from cakemail.wrapper import WrappedApi


class Workflow(WrappedApi):
    activate: WorkflowApi.activate_workflow
    create: WorkflowApi.create_workflow
    deactivate: WorkflowApi.deactivate_workflow
    delete: WorkflowApi.delete_workflow
    get: WorkflowApi.get_workflow
    list: WorkflowApi.list_workflows
    update: WorkflowApi.patch_workflow

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'activate': 'activate_workflow',
                'create': 'create_workflow',
                'deactivate': 'deactivate_workflow',
                'delete': 'delete_workflow',
                'get': 'get_workflow',
                'list': 'list_workflows',
                'update': 'patch_workflow',
            }
        )
