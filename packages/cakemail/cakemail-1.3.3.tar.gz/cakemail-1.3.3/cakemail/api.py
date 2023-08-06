import time

from cakemail_openapi import Configuration, ApiClient, TokenApi, AccountApi, ActionApi, CampaignApi, ContactApi, CustomAttributeApi, DomainApi, FormApi, ListApi, LogApi, LogoApi, ReportApi, SegmentApi, SenderApi, SubAccountApi, SuppressedEmailApi, UserApi, TemplateApi, TransactionalEmailApi, WorkflowApi
from .token import Token
from .account import Account
from .action import Action
from .campaign import Campaign
from .contact import Contact
from .custom_attribute import CustomAttribute
from .domain import Domain
from .form import Form
from .list import List
from .log import Log
from .logo import Logo
from .report import Report
from .segment import Segment
from .sender import Sender
from .sub_account import SubAccount
from .suppressed_email import SuppressedEmail
from .user import User
from .template import Template
from .transactional_email import TransactionalEmail
from .workflow import Workflow


class Api:
    _token = None

    account: Account
    action: Action
    campaign: Campaign
    contact: Contact
    custom_attribute: CustomAttribute
    domain: Domain
    form: Form
    list: List
    log: Log
    logo: Logo
    report: Report
    segment: Segment
    sender: Sender
    sub_account: SubAccount
    suppressed_email: SuppressedEmail
    user: User
    template: Template
    transactional_email: TransactionalEmail
    workflow: Workflow

    def __init__(
            self,
            username = None,
            password = None,
            url='https://api.cakemail.dev'
    ):
        self._config = Configuration(host=url)
        self._api_client = ApiClient(self._config)
        if username and password:
            self._token = Token(
                email=username,
                password=password,
                token_api=TokenApi(self._api_client),
                configuration=self._config
            )

        self.account = Account(AccountApi(self._api_client))
        self.action = Action(ActionApi(self._api_client))
        self.campaign = Campaign(CampaignApi(self._api_client))
        self.contact = Contact(ContactApi(self._api_client))
        self.custom_attribute = CustomAttribute(CustomAttributeApi(self._api_client))
        self.domain = Domain(DomainApi(self._api_client))
        self.form = Form(FormApi(self._api_client))
        self.list = List(ListApi(self._api_client))
        self.log = Log(LogApi(self._api_client))
        self.logo = Logo(LogoApi(self._api_client))
        self.report = Report(ReportApi(self._api_client))
        self.segment = Segment(SegmentApi(self._api_client))
        self.sender = Sender(SenderApi(self._api_client))
        self.sub_account = SubAccount(SubAccountApi(self._api_client))
        self.suppressed_email = SuppressedEmail(SuppressedEmailApi(self._api_client))
        self.user = User(UserApi(self._api_client))
        self.template = Template(TemplateApi(self._api_client))
        self.transactional_email = TransactionalEmail(TransactionalEmailApi(self._api_client))
        self.workflow = Workflow(WorkflowApi(self._api_client))

    def __getattribute__(self, name):
        if name not in ['_api_client', '_config', '_token']:
            if self._token and self._token.expires_at < time.time():
                self._token.refresh()

        return super(Api, self).__getattribute__(name)