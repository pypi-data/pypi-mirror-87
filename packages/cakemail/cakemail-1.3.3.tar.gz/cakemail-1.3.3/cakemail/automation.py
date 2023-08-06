from cakemail_openapi import AutomationApi
from cakemail.wrapper import WrappedApi


class Automation(WrappedApi):
    activate_workflow: AutomationApi.activate_workflow
    create_workflow: AutomationApi.create_workflow
    create_workflow_action: AutomationApi.create_workflow_action
    deactivate_workflow: AutomationApi.deactivate_workflow
    delete_workflow: AutomationApi.delete_workflow
    delete_workflow_action: AutomationApi.delete_workflow_action
    get_workflow: AutomationApi.get_workflow
    get_workflow_action: AutomationApi.get_workflow_action
    list_workflow_actions: AutomationApi.list_workflow_actions
    list_workflows: AutomationApi.list_workflows
    patch_workflow: AutomationApi.patch_workflow
    patch_workflow_action: AutomationApi.patch_workflow_action
    render_workflow_action: AutomationApi.render_workflow_action
    send_test_workflow_action: AutomationApi.send_test_workflow_action

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'activate_workflow': 'activate_workflow',
                'create_workflow': 'create_workflow',
                'create_workflow_action': 'create_workflow_action',
                'deactivate_workflow': 'deactivate_workflow',
                'delete_workflow': 'delete_workflow',
                'delete_workflow_action': 'delete_workflow_action',
                'get_workflow': 'get_workflow',
                'get_workflow_action': 'get_workflow_action',
                'list_workflow_actions': 'list_workflow_actions',
                'list_workflows': 'list_workflows',
                'patch_workflow': 'patch_workflow',
                'patch_workflow_action': 'patch_workflow_action',
                'render_workflow_action': 'render_workflow_action',
                'send_test_workflow_action': 'send_test_workflow_action',
            }
        )
