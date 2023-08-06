from cakemail_openapi import LogApi
from cakemail.wrapper import WrappedApi


class Log(WrappedApi):
    get_action: LogApi.get_action_logs
    get_campaign: LogApi.get_campaign_logs
    get_email: LogApi.get_email_logs
    get_list: LogApi.get_list_logs

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'get_action': 'get_action_logs',
                'get_campaign': 'get_campaign_logs',
                'get_email': 'get_email_logs',
                'get_list': 'get_list_logs',
            }
        )
