from dataclasses import dataclass
from logging import getLogger

from injector import inject

from core_get.actions.action import Action
from core_get.actions.login.login_options import LoginOptions
from core_get.configuration.credentials import Credentials
from core_get.configuration.credentials_accessor import CredentialsAccessor

logger = getLogger(__name__)


@inject
@dataclass
class Login(Action):
    credentials_accessor: CredentialsAccessor

    def exec(self, options: LoginOptions):
        credentials = Credentials(options.access_token)
        self.credentials_accessor.write(credentials)

        logger.info("Stored access token")
