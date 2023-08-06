from urllib.parse import urlparse

import typer

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.constants import DATASET_SOURCE_TYPE_SAVVIHUB, DATASET_PATH_PARSE_SCHEME_GS, \
    DATASET_PATH_PARSE_SCHEME_S3

dataset_app = typer.Typer()


def parse_dataset_arg(dataset_arg):
    if "/" not in dataset_arg:
        typer.echo("You should specify dataset with workspace. ex) savvihub/mnist")
        return
    workspace, rest = dataset_arg.split("/")
    if ":" in rest:
        dataset, ref = rest.split(":")
    else:
        dataset = rest
        ref = "latest"
    return workspace, dataset, ref


@dataset_app.callback()
def main():
    """
    Manage the collection of data
    """
    return


@dataset_app.command()
def create(
        dataset_arg: str = typer.Argument(...),
        path_arg: str = typer.Option(None, "-u", "--url", help="Dataset source path"),
        description: str = typer.Option(None, "-m", help="Dataset description"),
        aws_role_arn: str = typer.Option(None, "--aws-role-arn", help="AWS Role ARN")
):
    """
    Create a SavviHub dataset
    """
    workspace, dataset, _ = parse_dataset_arg(dataset_arg)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    if path_arg:
        if not (path_arg.startswith("gs://") or path_arg.startswith("s3://")):
            typer.echo(f"path should start with \"gs://\" or \"s3://\"")
            return

        r = urlparse(path_arg)
        if r.scheme == DATASET_PATH_PARSE_SCHEME_GS:
            dataset_obj = client.dataset_gs_create(workspace, dataset, False, description, path_arg)
        elif r.scheme == DATASET_PATH_PARSE_SCHEME_S3:
            if not aws_role_arn:
                typer.echo("AWS Role ARN is required for S3 users")
                return
            dataset_obj = client.dataset_s3_create(workspace, dataset, False, description, path_arg, aws_role_arn)
        else:
            raise Exception("Only Google Cloud Storage and Amazon S3 are supported at the moment.")
    else:
        dataset_obj = client.dataset_create(workspace, dataset, False, description)

    if not dataset_obj:
        return

    dataset_slug = dataset_obj.slug
    typer.echo(f"Dataset {dataset_slug} is created.")
    typer.echo(client.get_full_info_dataset(workspace, dataset_slug))

    return


@dataset_app.command()
def describe(
        dataset_arg: str = typer.Argument(...),
):
    """
    Describe the dataset information in detail
    """
    workspace, dataset, _ = parse_dataset_arg(dataset_arg)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    dataset = client.dataset_read(workspace, dataset)
    if not dataset:
        typer.echo('[Error]Dataset not found!\n You should specify dataset with workspace. ex) savvihub/mnist')

    typer.echo(
        f'Name: {dataset.slug}\n'
        f'Volume ID: {dataset.main_volume_id}\n'
        f'Workspace:\n'
        f'\tName: {dataset.workspace.slug}'
    )

    source = dataset.source
    if source.type != DATASET_SOURCE_TYPE_SAVVIHUB:
        typer.echo(
            f'Source:\n'
            f'\tType: {source.type}\n'
            f'\tPath: {source.bucket_name}/{source.path}'
        )
        typer.echo(f'{client.get_full_info_dataset(dataset.workspace.slug, dataset.slug)}')
