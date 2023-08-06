import os
import sys
import time
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

import typer

from savvihub import Context
from savvihub.api.errors import SavviHubNotADirectoryError
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.uploader import Downloader, Uploader
from savvihub.common.constants import ROLETYPE_DATASET_FILES, ROLETYPE_EXPERIMENT_OUTPUT, ROLETYPE_EXPERIMENT_INPUT, \
    DATASET_SOURCE_TYPE_SAVVIHUB
from savvihub.common.utils import parse_str_time_to_datetime, remove_suffix

volume_app = typer.Typer()


class PathException(Exception):
    pass


def refine_path(path_arg, raise_if_not_empty=False, raise_if_not_dir=False, raise_if_not_exist=False):
    if path_arg.startswith("savvihub://"):
        return path_arg, True

    path = os.path.abspath(path_arg)
    if os.path.exists(path):
        if not os.path.isdir(path) and raise_if_not_dir:
            raise PathException(f"Must specify directory: {path_arg}")
        if raise_if_not_empty and len(os.listdir(path)) > 0:
            raise PathException(f"Must specify empty directory: {path_arg}")
    else:
        if raise_if_not_exist:
            raise PathException(f"Must specify directory: {path_arg}")

    return path, False


def parse_remote_path(remote_path):
    u = urlparse(remote_path)
    volume_id = u.netloc
    path = u.path
    query = parse_qs(u.query)
    snapshot = query.get('snapshot', ['latest'])
    if len(snapshot) != 1:
        typer.echo(f'Invalid snapshots: {remote_path}')
    else:
        snapshot = snapshot[0]
    return volume_id, path, snapshot


@volume_app.callback()
def main():
    """
    Manage the mounted volumes
    """
    return


@volume_app.command()
def ls(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, "-r", help="recursive flag"),
    directory: bool = typer.Option(False, "-d", "--directory", help="list directories themselves, not their contents")
):
    """
    List files in the volume with prefix
    """
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, path, snapshot = parse_remote_path(source_path)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    if recursive and directory:
        typer.echo('[Error] -r and -d options cannot be used in one command')
        return
    elif recursive and not directory:
        files = client.volume_file_list(volume_id, snapshot=snapshot, path=path, recursive='true')
    elif not recursive and directory:
        if not path:
            typer.echo('[Error] path must be specified to run -d option')
            return
        files = [client.volume_file_read(volume_id, path, snapshot)]
    else:
        files = client.volume_file_list(volume_id, snapshot=snapshot, path=path, recursive='false')

    if not files or not files[0]:
        typer.echo('[Error] Entity Not Found!')
        return

    for file in files:
        typer.echo(file.path)
    return


@volume_app.command()
def describe(
    source_path_arg: str = typer.Argument(...),
):
    """
    Describe the volume information in detail
    """
    volume_id, path, _ = parse_remote_path(source_path_arg)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    volume = client.volume_read(volume_id)
    typer.echo(
        f'Volume ID: {volume.id}\n'
        f'Created: {parse_str_time_to_datetime(volume.created_dt)}\n'
        f'Updated: {parse_str_time_to_datetime(volume.updated_dt)}\n'
        f'Type: {volume.role_type}\n'
        f'Workspace:\n'
        f'\tName: {volume.workspace["slug"]}'
    )

    if volume.role_type == ROLETYPE_DATASET_FILES:
        dataset = volume.dataset
        typer.echo(
            f'Dataset:\n'
            f'\tName: {dataset["slug"]}\n'
            f'\tDescription: {dataset["description"]}'
        )

        source = dataset["source"]
        if source["type"] != DATASET_SOURCE_TYPE_SAVVIHUB:
            typer.echo(
                f'\tSource:\n'
                f'\t\tType: {source["type"]}\n'
                f'\t\tPath: {source["bucket_name"]}{source["path"]}'
            )
        typer.echo(f'{client.get_full_info_dataset(volume.workspace["slug"], volume.dataset["slug"])}')

    elif volume.role_type == ROLETYPE_EXPERIMENT_OUTPUT or volume.role_type == ROLETYPE_EXPERIMENT_INPUT:
        project = volume.project
        typer.echo(
            f'Project:\n'
            f'\tName: {project["slug"]}\n'
            f'\tDescription: {project["description"]}\n'
            f'\tGit repository: {project["git_http_url_to_repo"]}\n'
            f'{client.get_full_info_project(volume.workspace["slug"], project["slug"])}'
        )

        experiment = volume.experiment
        typer.echo(
            f'Experiment:\n'
            f'\tNumber: {experiment["number"]}\n'
            f'\tStatus: {experiment["status"]}\n'
            f'\tImage: {experiment["kernel_image"]["name"]}\n'
            f'\tResource: {experiment["kernel_resource_spec"]["name"]}\n'
            f'\tCommand: {experiment["start_command"]}\n'
            f'{client.get_full_info_experiment(volume.workspace["slug"], project["slug"], experiment["number"])}'
        )


@volume_app.command()
def rm(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, "-r", "-R", "--recursive",
                                   help="Remove directories and their contents recursively"),
):
    """
    Remove files in the volume with path
    """
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, path, snapshot = parse_remote_path(source_path)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    file = client.volume_file_read(volume_id, path, snapshot)

    if not file:
        typer.echo('[Error] Request entity not found')
        return

    if file.is_dir:
        if not recursive:
            typer.echo('[Error] Remove directory should use -r option')
            return
        deleted_files = client.volume_file_delete(volume_id, path, 'true')
    else:
        deleted_files = client.volume_file_delete(volume_id, path, 'false')

    if not deleted_files:
        typer.echo('[Error] Server error')
        return

    for file in deleted_files:
        typer.echo(f'{file.path}')

    return


@volume_app.command()
def cp(
    source_path_arg: str = typer.Argument(...),
    dest_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, "-r", "--recursive"),
    watch: bool = typer.Option(False, "-w", "--watch"),
):
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
        dest_path, is_dest_remote = refine_path(dest_path_arg)
    except PathException as e:
        typer.echo(str(e))
        return

    context = Context(login_or_experiment_required=True)
    hashmap = defaultdict(lambda: "")
    client = context.authorized_client

    while True:
        if is_source_remote and is_dest_remote:
            # remote -> remote
            source_volume_id, source_path, source_snapshot_ref = parse_remote_path(source_path)
            dest_volume_id, dest_path, dest_snapshot_ref = parse_remote_path(dest_path)
            if dest_snapshot_ref != 'latest':
                typer.echo(f'Cannot write to snapshots: {dest_path}')
                sys.exit(1)

            source_file = client.volume_file_read(source_volume_id, source_path, source_snapshot_ref)
            dest_file = client.volume_file_read(dest_volume_id, dest_path, dest_snapshot_ref)
            if source_file is None:
                typer.echo(f'Source file does not exist: {source_path}')
                sys.exit(1)

            if source_file.is_dir and not recursive:
                typer.echo(f'Source path is a directory, you should call with --recursive option.')
                sys.exit(1)

            if source_file.is_dir and dest_file is not None and not dest_file.is_dir:
                typer.echo(f'Source path is a directory, but destination path is a file.')
                sys.exit(1)

            client.volume_file_copy(source_volume_id, source_file.path, source_snapshot_ref, dest_path, recursive=recursive)

        elif is_source_remote and not is_dest_remote:
            # remote -> local
            source_volume_id, source_path, source_snapshot_ref = parse_remote_path(source_path)
            source_file = client.volume_file_read(source_volume_id, source_path, source_snapshot_ref)

            if source_file is None:
                typer.echo(f'Source file does not exist: {source_path}')
                sys.exit(1)

            if source_file.is_dir:
                if not recursive:
                    typer.echo(f'Source path is a directory, you should call with --recursive option.')
                    sys.exit(1)

                if os.path.exists(dest_path) and not os.path.isdir(dest_path):
                    typer.echo(f'Destination path is not a directory: {dest_path}')
                    sys.exit(1)

                # download directory
                typer.echo('Fetching file metadata...')
                files = client.volume_file_list(source_volume_id, path=source_path, snapshot=source_snapshot_ref, recursive=True, need_download_url=True)
                files = [file for file in files if hashmap[file.path] != file.hash]

                typer.echo(f'Find {len(files)} files to download.')
                typer.echo('Downloading...')
                if len(files) > 0:
                    Downloader.bulk_download(context, dest_path, files, progressable=typer.progressbar)
                    for file in files:
                        hashmap[file.path] = file.hash
                typer.echo('Download completed.')
            else:
                # download file
                if os.path.exists(dest_path):
                    if os.path.isdir(dest_path):
                        dest_file_path = os.path.join(dest_path, os.path.basename(source_file.path))
                    else:
                        dest_file_path = dest_path
                else:
                    dest_file_path = dest_path

                Downloader.download(dest_file_path, source_file, progressable=typer.progressbar)
                hashmap[source_file.path] = source_file.hash

        elif not is_source_remote and is_dest_remote:
            # local -> remote
            dest_volume_id, dest_path, dest_snapshot_ref = parse_remote_path(dest_path)
            if dest_snapshot_ref != 'latest':
                typer.echo(f'Cannot write to snapshots: {dest_path}')
                sys.exit(1)

            try:
                dest_file = client.volume_file_read(dest_volume_id, dest_path, dest_snapshot_ref)
            except SavviHubNotADirectoryError:
                typer.echo(f'{dest_path} is a file, not a directory.')
                sys.exit(1)

            if not os.path.exists(source_path):
                typer.echo(f'Source file does not exist: {source_path}')
                sys.exit(1)

            if os.path.isdir(source_path):
                if not recursive:
                    typer.echo(f'Source path is a directory, you should call with --recursive option.')
                    sys.exit(1)

                files = Uploader.get_files_to_upload(source_path, hashmap)
                if dest_file is None:
                    # x/y/dir1/ -> c/ (not exist)
                    # x/y/dir1/file1/ -> c/file1
                    dest_base_path = dest_path
                elif dest_file.is_dir:
                    # x/y/dir1/ -> c/ (exist path)
                    # x/y/dir1/file1/ -> c/dir1/file1
                    dest_base_path = os.path.join(dest_path, os.path.basename(remove_suffix(source_path, "/")))
                else:
                    typer.echo(f'Destination path is not directory: {dest_path}')
                    sys.exit(1)

                typer.echo(f'Find {len(files)} files to upload.')
                typer.echo('Uploading...')
                if len(files) > 0:
                    Uploader.bulk_upload(context, source_path, files, dest_volume_id, dest_base_path, progressable=typer.progressbar)
                    hashmap = Uploader.get_hashmap(source_path)
                typer.echo('Upload completed.')
            else:
                # x/y/dir1/file1 ->
                if dest_file is None:
                    if dest_path.endswith('/'):
                        Uploader.upload(context, source_path, dest_volume_id, os.path.join(dest_path, os.path.basename(source_path)))
                    else:
                        Uploader.upload(context, source_path, dest_volume_id, dest_path)
                elif dest_file.is_dir:
                    Uploader.upload(context, source_path, dest_volume_id, dest_path)
                else:
                    Uploader.upload(context, source_path, dest_volume_id, os.path.join(dest_path, os.path.basename(source_path)))

        else:
            typer.echo('Cannot copy volume from local to local')
            return

        if not watch:
            return

        time.sleep(10)
