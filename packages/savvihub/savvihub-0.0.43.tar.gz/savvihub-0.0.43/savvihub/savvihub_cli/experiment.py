import os
import re
import sys
import tempfile
from typing import List

import inquirer
import typer
from terminaltables import AsciiTable

from savvihub.api.file_object import DownloadableFileObject
from savvihub.api.uploader import Uploader
from savvihub.common.constants import INQUIRER_NAME_COMMAND, WEB_HOST
from savvihub.common.context import Context
from savvihub.common.formatter import TreeFormatter
from savvihub.common.utils import short_string, parse_time_to_ago, parse_str_time_to_datetime, \
    parse_timestamp_or_none
from savvihub.savvihub_cli.errors import get_error_message
from savvihub.savvihub_cli.volumes import volume_file_list, volume_file_copy

experiment_output_app = typer.Typer()
experiment_app = typer.Typer()
experiment_app.add_typer(experiment_output_app, name='output')


@experiment_app.callback()
def main():
    """
    Run the machine learning experiment
    """
    return


@experiment_app.command()
def list():
    """
    Display a list of experiments
    """

    context = Context(login_required=True, project_required=True)
    client = context.authorized_client

    experiments = client.experiment_list(context.project.workspace.slug, context.project.slug, raise_error=True)
    table = AsciiTable([
        ['NUMBER', 'STATUS', 'CREATED', 'IMAGE', 'RESOURCE', 'START COMMAND'],
        *[[e.number, e.status, parse_time_to_ago(e.created_dt),  short_string(e.kernel_image.name, 25),
           e.kernel_resource_spec.name, f'"{short_string(e.start_command, 25)}"']
          for e in experiments],
    ])
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = False
    table.outer_border = False

    typer.echo(table.table)


@experiment_app.command()
def describe(
    experiment_number: int = typer.Argument(..., help="The unique experiment number"),
):
    """
    Describe the experiment in details
    """
    context = Context(login_required=True, project_required=True)
    client = context.authorized_client

    experiment = client.experiment_read(
        context.project.workspace.slug, context.project.slug, experiment_number,
        raise_error=True,
    )

    root = TreeFormatter()
    root.add_child(f'Number: {experiment.number}',
                   f'Created: {parse_str_time_to_datetime(experiment.created_dt)}',
                   f'Updated: {parse_str_time_to_datetime(experiment.updated_dt)}',
                   f'Message: {experiment.message}',
                   f'Status: {experiment.status}',
                   f'Tensorboard: {experiment.tensorboard or "N/A"}',
                   f'Tensorboard log_dir: {experiment.tensorboard_log_dir or "N/A"}')

    # Kernel Image Description
    kernel_image_desc = TreeFormatter('Kernel Image:')
    kernel_image_desc.add_child(f'Name: {experiment.kernel_image.name}',
                                f'URL: {experiment.kernel_image.image_url}',
                                f'Language: {experiment.kernel_image.language}')
    root.add_child(kernel_image_desc)

    # Resource Spec Description
    resource_spec_desc = TreeFormatter('Resource Spec:')
    resource_spec_desc.add_child(f'Name: {experiment.kernel_resource_spec.name}',
                                 f'CPU Type: {experiment.kernel_resource_spec.name}',
                                 f'CPU Limit: {experiment.kernel_resource_spec.cpu_limit}',
                                 f'CPU Guarantee: {experiment.kernel_resource_spec.cpu_guarantee}',
                                 f'Memory Limit: {experiment.kernel_resource_spec.mem_limit}',
                                 f'Memory Guarantee: {experiment.kernel_resource_spec.mem_guarantee}',
                                 f'GPU Type: {experiment.kernel_resource_spec.gpu_type}',
                                 f'GPU Limit: {experiment.kernel_resource_spec.gpu_limit}',
                                 f'GPU Guarantee: {experiment.kernel_resource_spec.gpu_guarantee}')
    root.add_child(resource_spec_desc)

    # Datasets Description
    datasets_desc = TreeFormatter('Datasets:')
    if not experiment.datasets:
        datasets_desc.add_child('Dataset Not Found')
    else:
        for dataset in experiment.datasets:
            dataset_desc = TreeFormatter(dataset['dataset_slug'])
            dataset_desc.add_child(f'Mount Path: {dataset["mount_path"]}')
            datasets_desc.add_child(dataset_desc)
    root.add_child(datasets_desc)

    # Histories Description
    histories_desc = TreeFormatter('Histories:')
    if not experiment.histories:
        histories_desc.add_child('History Not Found')
    else:
        for history in experiment.histories:
            history_desc = TreeFormatter(history['status'])
            history_desc.add_child(f'Started: {parse_timestamp_or_none(history["started_timestamp"])}',
                                   f'Ended: {parse_timestamp_or_none(history["ended_timestamp"])}')
            histories_desc.add_child(history_desc)
    root.add_child(histories_desc)

    # Metrics Description
    metrics_desc = TreeFormatter('Metrics:')
    if not experiment.metrics:
        metrics_desc.add_child('Metrics Not Found')
    else:
        for history in experiment.metrics[-10:]:
            metrics_desc.add_child(history)

        full_metrics_info_desc = TreeFormatter('Full metrics info at:')
        full_metrics_info_desc.add_child(f'{WEB_HOST}/{context.project.workspace.slug}/{context.project.slug}/experiments/{experiment.number}/metrics')
        metrics_desc.add_child(full_metrics_info_desc)
    root.add_child(metrics_desc)

    # System Metrics Description
    system_metrics_desc = TreeFormatter('System Metrics:')
    full_system_metrics_info_desc = TreeFormatter('Full system metrics info at:')
    full_system_metrics_info_desc.add_child(f'{WEB_HOST}/{context.project.workspace.slug}/{context.project.slug}/experiments/{experiment.number}/system-metrics')
    system_metrics_desc.add_child(full_system_metrics_info_desc)
    root.add_child(system_metrics_desc)
    root.add_child(f'Start Command: {experiment.start_command}',
                   f'Source Code Link: {experiment.source_code_link}')

    typer.echo(root.format())


@experiment_app.command()
def logs(
    experiment_number: int = typer.Argument(..., help="The unique experiment number"),
    tail: int = typer.Option(200, "--tail"),
    detail: bool = typer.Option(False, "--detail", hidden=True),
    all: bool = typer.Option(False, "--all", hidden=True),
):
    """
    Display the last fifty lines of the experiment logs
    """
    context = Context(login_required=True, project_required=True)
    client = context.authorized_client

    if not all:
        params = {'limit': tail}
    if detail:
        params = {'withEventLog': 'true'}

    experiment_logs = client.experiment_log(
        context.project.workspace.slug, context.project.slug, experiment_number, params=params, raise_error=True)

    for log in experiment_logs:
        typer.echo(f'{parse_timestamp_or_none(log.timestamp)} {log.message}')

    typer.echo(
        client.get_full_info(context.project.workspace.slug, context.project.slug, experiment_number, 'logs')
    )


@experiment_app.command()
def run(
    command_arg: str = typer.Option(None, "-c", help="Start command"),
    image_arg: str = typer.Option(None, "-i", help="Kernel image URL"),
    resource_arg: str = typer.Option(None, "-r", help="Resource name"),
    env_vars_arg: List[str] = typer.Option([], "-e", help="Environment variables"),
    dataset_mount_args: List[str] = typer.Option([], "--dataset", help="Dataset mounted path"),
    git_ref_arg: str = typer.Option(None, "--git-ref", help="Git commit SHA"),
    git_diff_arg: str = typer.Option(None, "--git-diff", help="Git diff file URL"),
    ignore_git_diff_arg: bool = typer.Option(False, "--ignore-git-diff", help="Ignore git diff flag"),
):
    """
    Run an experiment in SavviHub
    """
    context = Context(login_required=True, project_required=True)
    client = context.authorized_client

    def find_from_args(options, selector, error_message=''):
        for option in options:
            if selector(option):
                return option

        if error_message:
            typer.echo(error_message)
            sys.exit(1)

    def find_from_inquirer(options, display):
        answers = inquirer.prompt([inquirer.List(
            "question",
            message="Please choose a kernel image",
            choices=[f'[{i+1}] {display(option)}' for i, option in enumerate(options)],
        )])
        answer = int(re.findall(r"[\d+]", answers.get("question"))[0]) - 1
        return options[answer]

    selected_image_url, selected_resource, start_command = None, None, None

    resources = client.kernel_resource_list(context.project.workspace.slug)
    if resource_arg:
        selected_resource = find_from_args(
            resources,
            lambda x: x.name == resource_arg.strip(),
            error_message=f'Cannot find resource {resource_arg}.',
        )
    else:
        selected_resource = find_from_inquirer(
            resources,
            lambda x: f'{x.name} ({x.description})',
        )

    images = client.kernel_image_list(context.project.workspace.slug, selected_resource.processor_type)
    if not image_arg:
        selected_image_url = find_from_inquirer(
            images,
            lambda x: f'{x.image_url} ({x.name})',
        ).image_url
    else:
        selected_image_url = image_arg.strip()

    if command_arg:
        start_command = command_arg
    else:
        answers = inquirer.prompt([inquirer.Text(
            INQUIRER_NAME_COMMAND,
            message="Start command",
            default="python main.py",
        )])
        answer = answers.get(INQUIRER_NAME_COMMAND)
        start_command = answer

    dataset_mounts_parsed = []
    for dataset_mount in dataset_mount_args:
        # parse dataset and volume
        if ':' not in dataset_mount:
            typer.echo(f'Invalid dataset slug: {dataset_mount}. '
                       f'You should specify dataset and mount location.\n'
                       f'ex) savvihub/mnist:3d1e0f:/input/dataset1')
            sys.exit(1)

        # parse snapshot ref
        splitted = dataset_mount.split(':')
        if len(splitted) == 2:
            dataset_slug_with_workspace, mount_path = splitted
            snapshot_ref = 'latest'
        elif len(splitted) == 3:
            dataset_slug_with_workspace, snapshot_ref, mount_path = splitted
        else:
            typer.echo(f'Invalid dataset slug: {dataset_mount}\n'
                       f'You should specify dataset and mount location.\n'
                       f'ex) savvihub/mnist:3d1e0f:/input/dataset1')
            sys.exit(1)

        if '/' not in dataset_slug_with_workspace:
            typer.echo(f'Invalid dataset slug: {dataset_mount}\n'
                       f'You should specify dataset with workspace.\n'
                       f'ex) savvihub/mnist:3d1e0f:/input/dataset1')
            sys.exit(1)

        workspace_slug, dataset_slug = dataset_slug_with_workspace.split('/')

        # read dataset or snapshot
        dataset_obj = client.dataset_read(workspace_slug, dataset_slug)
        if not dataset_obj:
            typer.echo(f'Invalid dataset: {dataset_slug_with_workspace}\n'
                       f'Please check your dataset exist in savvihub.\n')
            sys.exit(1)

        if snapshot_ref != 'latest':
            snapshot_obj = client.snapshot_read(dataset_obj.main_volume_id, snapshot_ref)
            if not snapshot_obj:
                typer.echo(f'Invalid dataset snapshots: {dataset_mount}\n'
                           f'Please check your dataset and snapshot exist in savvihub.')
                sys.exit(1)

        if not mount_path.startswith('/input'):
            typer.echo(f'Invalid dataset mount path: {mount_path}\n'
                       f'Dataset mount path should start with /input.')
            sys.exit(1)

        dataset_mounts_parsed.append(dict(
            dataset_id=dataset_obj.id,
            snapshot_ref=snapshot_ref,
            mount_path=mount_path,
        ))

    git_ref = None
    diff_file = None
    if git_ref_arg:
        if not context.git_repo.check_revision_in_remote(git_ref_arg.strip()):
            typer.echo(f'Git commit {git_ref_arg.strip()} does not exist in a remote repository.')
            sys.exit(1)

        git_ref = git_ref_arg.strip()

        if git_diff_arg:
            if git_diff_arg.startswith("https://") or \
                    git_diff_arg.startswith("http://"):
                diff_file = tempfile.NamedTemporaryFile(suffix=".patch")
                d = DownloadableFileObject(git_diff_arg, os.path.dirname(diff_file.name),
                                           os.path.basename(diff_file.name))
                d.download(session=context.authorized_client.session)
                diff_file.seek(0)

    else:
        git_ref, branch, is_head = context.git_repo.get_remote_revision_or_branch()
        commit = context.git_repo.get_commit_message(git_ref)
        typer.echo(f'Run experiment with revision {git_ref[:6]} ({branch})')
        typer.echo(f'Commit: {commit}')
        if not is_head:
            typer.echo('Your current revision does not exist in remote repository. SavviHub will use latest remote '
                       'branch revision hash and diff.')
        typer.echo('')

        has_diff, diff_status = context.git_repo.get_current_diff_status(git_ref)
        if has_diff and not ignore_git_diff_arg:
            typer.echo('Diff to be uploaded: ')

            uncommitted_files = diff_status.get('uncommitted')
            untracked_files = diff_status.get('untracked')

            if uncommitted_files:
                typer.echo('  Changes not committed')
                typer.echo("\n".join([f'    {x}' for x in uncommitted_files]))
                typer.echo("")
            if untracked_files:
                typer.echo(f'  Untracked files:')
                typer.echo("\n".join([f'    {x}' for x in untracked_files]))
                typer.echo("")

            # TODO: reduce choices if uncommited or untracked not exist

            answers = inquirer.prompt([inquirer.List(
                "experiment",
                message="Run experiment with diff?",
                choices=[
                    '[1] Run experiment with uncommitted and untracked changes.',
                    '[2] Run experiment with uncommitted changes.',
                    '[3] Run experiment without any changes.',
                    '[4] Abort.',
                ],
            )])
            answer = int(re.findall(r"[\d+]", answers.get("experiment"))[0])

            diff_file = None
            if answer == 1:
                diff_file = context.git_repo.get_current_diff_file(git_ref, with_untracked=True)
            elif answer == 2:
                diff_file = context.git_repo.get_current_diff_file(git_ref, with_untracked=False)
            elif answer == 3:
                pass
            elif answer == 4:
                typer.echo('Aborted.')
                return

    input_volume_id = None
    diff_file_path = None
    if diff_file:
        typer.echo('Generating diff patch file...')
        volume = client.volume_create(context.project.workspace.slug)
        input_volume_id = volume.id
        uploaded = Uploader.parallel_upload(
            context,
            os.path.dirname(diff_file.name),
            [os.path.basename(diff_file.name)],
            volume.id,
            progressable=typer.progressbar,
        )
        diff_file_path = uploaded[0].path
        diff_file.close()

    env_vars = []
    for env_var in env_vars_arg:
        try:
            env_key, env_value = env_var.split("=")
            env_vars.append({
                'key': env_key,
                'value': env_value,
            })
        except:
            typer.echo(f'Cannot parse environment variable: {env_var}')
            sys.exit(1)

    res = client.experiment_create(
        workspace=context.project.workspace.slug,
        project=context.project.slug,
        image_url=selected_image_url,
        resource_spec_id=selected_resource.id,
        git_ref=git_ref,
        git_diff_file_path=diff_file_path,
        input_volume_id=input_volume_id,
        start_command=start_command,
        dataset_mount_infos=dataset_mounts_parsed,
        env_vars=env_vars,
    )

    res_data = res.json()
    if res.status_code == 400:
        typer.echo(get_error_message(res_data))
        sys.exit(1)

    res.raise_for_status()

    experiment_number = res_data.get('number')
    typer.echo(f"Experiment {experiment_number} is running. Check the experiment status at below link")
    typer.echo(f"{WEB_HOST}/{context.project.workspace.slug}/{context.project.slug}/"
               f"experiments/{experiment_number}")
    return


@experiment_output_app.callback()
def output_main():
    """
    Manage experiment output files
    """


@experiment_output_app.command()
def ls(
    experiment_number: int = typer.Argument(..., help="The unique experiment number"),
    path: str = typer.Argument(None, help='Output file path'),
    recursive: bool = typer.Option(False, '-r', '--recursive', help='recursive flag'),
    directory: bool = typer.Option(False, '-d', '--directory',
                                   help='list the directory itself, not its contents'),
):
    """
    List the output files of the experiment
    """
    context = Context(login_required=True, project_required=True)
    client = context.authorized_client

    experiment = client.experiment_read(
        context.project.workspace.slug, context.project.slug, experiment_number, raise_error=True,
    )
    volume_file_list(experiment.output_volume_id, 'latest', path or '', recursive, directory)


@experiment_output_app.command()
def download(
    experiment_number: int = typer.Argument(..., help='The unique experiment number'),
    dest_path: str = typer.Argument(None, help='The files will be downloaded to ./output if omitted.'),
):
    """
    Download experiment output files
    """
    context = Context(login_required=True, project_required=True)
    client = context.authorized_client

    experiment = client.experiment_read(
        context.project.workspace.slug, context.project.slug, experiment_number, raise_error=True,
    )
    volume_file_copy(experiment.output_volume_id, 'latest', '',
                     None, None, dest_path or './output',
                     recursive=True, watch=False)


if __name__ == "__main__":
    experiment_app()
