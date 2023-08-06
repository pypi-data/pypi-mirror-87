from typing import Optional, Union, Iterable, Text, IO, Any, Mapping
from unittest import TestCase

from click.testing import Result
from typer.testing import CliRunner as TyperCliRunner

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.utils import random_string
from savvihub.savvihub_cli.main import app


class CliRunner(TyperCliRunner):
    def invoke(
        self,
        args: Optional[Union[str, Iterable[str]]] = None,
        input: Optional[Union[bytes, Text, IO[Any]]] = None,
        env: Optional[Mapping[str, str]] = None,
        color: bool = False,
        **extra: Any,
    ) -> Result:
        return super().invoke(app, args, input, env, catch_exceptions=False, color=color, **extra)


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self._auto_savvi_init()
        self._monkey_patch(self.token, self.workspace_slug, self.project_slug)
        self.context = Context(login_required=True, project_required=True)
        self.client = SavviHubClient(token=self.context.token)
        self.runner = CliRunner()

    def _auto_savvi_init(self):
        # user init
        username = random_string()
        jwt_client = SavviHubClient()
        r = jwt_client.post('/api/v1/accounts/signup', {
            'email': f'{username}@savvihub.test',
            'username': username,
            'name': username,
            'password': 'testtest',
            'invitation_token': 'invitation_token_for_cli_test',
        }, raise_error=True).json()
        jwt_client.session.headers['Authorization'] = f'JWT {r["token"]}'

        cli_token = jwt_client.check_signin_token()
        jwt_client.post('/api/v1/accounts/signin/cli/confirm', {
            'cli_token': cli_token,
        }, raise_error=True)

        success, access_token = jwt_client.check_signin(cli_token)
        if not success:
            raise Exception('Signin Failed')

        # project init
        access_token_client = SavviHubClient(token=access_token)
        workspace_slug = access_token_client.workspace_list()[0].slug
        project_slug = random_string()
        me = access_token_client.get_my_info()
        access_token_client.project_github_create(workspace_slug, project_slug, me.username, project_slug)

        self.token = access_token
        self.workspace_slug = workspace_slug
        self.project_slug = project_slug

    def _monkey_patch(self, token, workspace_slug, project_slug):
        class MockConfig:
            def __init__(self):
                self.token = token
                self.workspace = workspace_slug
                self.project = project_slug

        def context_init(
            self,
            login_required=False,
            project_required=False,
            experiment_required=False,
            login_or_experiment_required=False,
        ):
            mock_config = MockConfig()
            if login_required:
                self.global_config = mock_config
                self.user = self.get_my_info()

            if project_required:
                self.git_repo = None  # TODO
                self.project_config = mock_config
                self.project = self.get_project()

            if experiment_required:
                raise NotImplemented('Please implement this..')

            if login_or_experiment_required:
                raise NotImplemented('Please implement this..')

        Context.__init__ = context_init
