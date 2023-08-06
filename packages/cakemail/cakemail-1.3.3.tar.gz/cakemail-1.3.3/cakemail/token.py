import time

from cakemail_openapi import TokenApi, Configuration


class Token:
    email = None
    password = None
    account_id = None
    access_token = None
    refresh_token = None
    expires_at = 0
    token_api = None

    def __init__(
            self,
            email: str = None,
            password: str = None,
            refresh_token: str = None,
            account_id: int = None,
            token_api: TokenApi = None,
            configuration: Configuration = None
    ):
        """ Token object; creates, stores and refreshes the user's token """
        self.email = email
        self.password = password
        self.refresh_token = refresh_token
        self.account_id = account_id
        self.token_api = token_api
        self.configuration = configuration

    def create(self):
        """ Create the initial token """
        if self.refresh_token and not self.email and not self.password:
            response = self.token_api.refresh_token(
                refresh_token=self.refresh_token
            )
        else:
            credentials = {
                'username': self.email,
                'password': self.password
            }
            if self.account_id:
                credentials['client_id'] = self.account_id

            response = self.token_api.create_token(**credentials)

        self.access_token = response.access_token
        self.refresh_token = response.refresh_token
        self.expires_at = time.time() + response.expires_in
        self.configuration.access_token = self.access_token

    def refresh(self):
        """ Refresh the token """
        if self.refresh_token:
            response = self.token_api.refresh_token(
                refresh_token=self.refresh_token
            )
            self.access_token = response.access_token
            self.refresh_token = response.refresh_token
            self.expires_at = time.time() + response.expires_in
            self.configuration.access_token = self.access_token
        else:
            self.create()
