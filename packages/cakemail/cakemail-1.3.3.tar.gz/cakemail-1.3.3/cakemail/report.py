from cakemail_openapi import ReportApi
from cakemail.wrapper import WrappedApi


class Report(WrappedApi):
    get_account: ReportApi.get_account_stats
    get_action: ReportApi.get_action_stats
    get_campaign_link: ReportApi.get_campaign_links_stats
    get_campaign: ReportApi.get_campaign_stats
    get_email: ReportApi.get_emails_stats
    get_list: ReportApi.get_list_stats
    get_self_account: ReportApi.get_self_account_stats

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'get_account': 'get_account_stats',
                'get_action': 'get_action_stats',
                'get_campaign_link': 'get_campaign_links_stats',
                'get_campaign': 'get_campaign_stats',
                'get_email': 'get_emails_stats',
                'get_list': 'get_list_stats',
                'get_self_account': 'get_self_account_stats',
            }
        )
