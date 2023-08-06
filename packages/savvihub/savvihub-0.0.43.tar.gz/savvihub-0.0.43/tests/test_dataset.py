from savvihub.common.constants import WEB_HOST
from savvihub.common.utils import random_string
from tests.conftest import BaseTestCase


class DatasetTest(BaseTestCase):
    def test_dataset(self):
        # Check current datasets
        result = self.runner.invoke(['dataset', 'list'])
        assert result.exit_code == 0
        initial_line_count = len(result.output.split('\n'))

        # Missing argument
        result = self.runner.invoke(['dataset', 'create'])
        assert "Error: Missing argument 'DATASET_ARG'" in result.output

        dataset1_name = random_string()
        # Invalid dataset formats
        result = self.runner.invoke(['dataset', 'create', f'aa://{self.workspace_slug}/{dataset1_name}/'])
        assert result.exit_code == 1
        assert 'Invalid dataset name format.' in result.output
        result = self.runner.invoke(['dataset', 'create', f'{self.workspace_slug}//{dataset1_name}/'])
        assert result.exit_code == 1
        assert 'Invalid dataset name format.' in result.output

        # Valid dataset formats
        result = self.runner.invoke(['dataset', 'create', f'svds://{self.workspace_slug}/{dataset1_name}/'])
        assert f'Dataset {dataset1_name} is created.' in result.output
        assert f'{WEB_HOST}/{self.workspace_slug}/datasets/{dataset1_name}' in result.output
        dataset_name = random_string()
        result = self.runner.invoke(['dataset', 'create', f'{self.workspace_slug}/{dataset_name}'])
        assert f'Dataset {dataset_name} is created.' in result.output
        assert f'{WEB_HOST}/{self.workspace_slug}/datasets/{dataset_name}' in result.output

        # Two datasets have been created
        result = self.runner.invoke(['dataset', 'list'])
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == initial_line_count + 2
