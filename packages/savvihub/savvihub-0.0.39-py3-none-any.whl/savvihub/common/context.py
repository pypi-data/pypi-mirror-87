import os
from typing import Optional

from savvihub.api.types import SavviHubUser, SavviHubProject
from savvihub.common.git import GitRepository
from savvihub.common.config_loader import GlobalConfigLoader, ProjectConfigLoader
from savvihub.common.experiment import Experiment


class Value:
    def __init__(self, global_config_yml=None, savvihub_file_yml=None, env=None, computed=None, default_value=None):
        self.global_config_yml = global_config_yml
        self.savvihub_file_yml = savvihub_file_yml
        self.env = env
        self.computed = computed
        self.default_value = default_value


class Context:
    global_config = None
    project_config = None
    git_repo = None

    user: Optional[SavviHubUser] = None
    project: Optional[SavviHubProject] = None
    experiment: Optional[Experiment] = None

    experiment_token = os.environ.get("EXPERIMENT_ACCESS_TOKEN", None)
    parallel = os.environ.get("PARALLEL", 20)

    def __init__(self, login_required=False, project_required=False, experiment_required=False,
                 login_or_experiment_required=False):
        if login_required:
            self.global_config = self.load_global_config()
            self.user = self.get_my_info()

            if self.user is None:
                if self.global_config.token:
                    raise Exception('Login required. You should call `savvi init` first.')
                else:
                    raise Exception('Token expired. You should call `savvi init` first.')

        if project_required:
            self.git_repo = GitRepository()
            self.project_config = self.load_project_config(self.git_repo.get_savvihub_config_file_path())
            self.project = self.get_project()

            if self.project is None:
                raise Exception('Project not found. Run `savvi project init`.')

        if experiment_required:
            self.experiment = self.get_experiment()

            if self.experiment is None:
                raise Exception('Experiment token required.')

        if login_or_experiment_required:
            self.global_config = self.load_global_config()
            self.user = self.get_my_info()
            self.experiment = self.get_experiment()

            if self.user is None and self.experiment is None:
                if self.global_config.token:
                    raise Exception('Login required. You should call `savvi init` first.')
                else:
                    raise Exception('Token expired. You should call `savvi init` first.')


    def get_my_info(self):
        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.global_config.token)
        return client.get_my_info()

    def get_experiment(self):
        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.experiment_token)

        experiment = client.experiment_token_read(raise_error=True)
        if experiment is None:
            return None

        return Experiment.from_given(experiment, client)

    def get_project(self):
        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.global_config.token)
        project = client.project_read(self.project_config.workspace, self.project_config.project)
        return project

    @property
    def authorized_client(self):
        from savvihub.api.savvihub import SavviHubClient
        return SavviHubClient(token=self.token)

    @property
    def token(self):
        if self.experiment_token:
            return self.experiment_token
        return self.global_config.token

    @staticmethod
    def load_global_config():
        return GlobalConfigLoader()

    @staticmethod
    def load_project_config(project_config_path):
        if not project_config_path:
            return None
        return ProjectConfigLoader(project_config_path)
