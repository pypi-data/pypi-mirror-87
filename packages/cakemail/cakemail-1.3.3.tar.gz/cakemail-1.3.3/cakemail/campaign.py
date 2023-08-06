from cakemail_openapi import CampaignApi
from cakemail.wrapper import WrappedApi


class Campaign(WrappedApi):
    archive: CampaignApi.archive_campaign
    cancel: CampaignApi.cancel_campaign
    create: CampaignApi.create_campaign
    delete: CampaignApi.delete_campaign
    get: CampaignApi.get_campaign
    list: CampaignApi.list_campaigns
    list_links: CampaignApi.list_links
    update: CampaignApi.patch_campaign
    render: CampaignApi.render_campaign
    reschedule: CampaignApi.reschedule_campaign
    resume: CampaignApi.resume_campaign
    schedule: CampaignApi.schedule_campaign
    send_test_email: CampaignApi.send_test_email
    suspend: CampaignApi.suspend_campaign
    unarchive: CampaignApi.unarchive_campaign
    unschedule: CampaignApi.unschedule_campaign

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'archive': 'archive_campaign',
                'cancel': 'cancel_campaign',
                'create': 'create_campaign',
                'delete': 'delete_campaign',
                'get': 'get_campaign',
                'list': 'list_campaigns',
                'list_links': 'list_links',
                'update': 'patch_campaign',
                'render': 'render_campaign',
                'reschedule': 'reschedule_campaign',
                'resume': 'resume_campaign',
                'schedule': 'schedule_campaign',
                'send_test_email': 'send_test_email',
                'suspend': 'suspend_campaign',
                'unarchive': 'unarchive_campaign',
                'unschedule': 'unschedule_campaign',
            }
        )
