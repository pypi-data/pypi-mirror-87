import json
import os
import shutil
from argparse import ArgumentParser, HelpFormatter
from datetime import datetime
from functools import partial
from typing import Sequence

from pathlib2 import Path

from trains.datasets import Dataset


def print_args(args, exclude=('command', 'func', 'verbose')):
    # type: (object, Sequence[str]) -> ()
    if not getattr(args, 'verbose', None):
        return
    for arg in args.__dict__:
        if arg in exclude or args.__dict__.get(arg) is None:
            continue
        print('{}={}'.format(arg, args.__dict__[arg]))


def main():
    # type: () -> int
    title = 'Trains-Data - Dataset versioning CLI'
    print(title)
    parser = ArgumentParser(  # noqa
        description=title,
        prog='trains-data',
        formatter_class=partial(HelpFormatter, indent_increment=0, max_help_position=10),
    )
    subparsers = parser.add_subparsers(help='Dataset actions', dest='command')

    create = subparsers.add_parser('create', help='Create a new dataset')
    create.add_argument('--parents', type=str, nargs='*', help='Specify dataset parents IDs (i.e. merge all parents)')
    create.add_argument('--project', type=str, required=True, default=None, help='Dataset project name')
    create.add_argument('--name', type=str, required=True, default=None, help='Dataset name')
    create.add_argument('--tags', type=str, nargs='*', help='Dataset user Tags')
    create.set_defaults(func=ds_create)

    add = subparsers.add_parser('add', help='Add files to the dataset')
    add.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    add.add_argument('--dataset-folder', type=str, default=None,
                     help='Dataset base folder top add the files to (default: Dataset root)')
    add.add_argument('--files', type=str, nargs='*',
                     help='Files / folders to add (support for wildcard selection). '
                          'Example: ~/data/*.jpg ~/data/jsons')
    add.add_argument('--non-recursive', action='store_true', default=False,
                     help='Disable recursive scan of files')
    add.add_argument('--verbose', action='store_true', default=False, help='Verbose reporting')
    add.set_defaults(func=ds_add)

    sync = subparsers.add_parser('sync', help='Sync a local folder with the dataset')
    sync.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    sync.add_argument('--dataset-folder', type=str, default=None,
                      help='Dataset base folder top add the files to (default: Dataset root)')
    sync.add_argument('--folder', type=str, required=True,
                      help='Local folder to sync (support for wildcard selection). '
                           'Example: ~/data/*.jpg')
    sync.add_argument('--verbose', action='store_true', default=False, help='Verbose reporting')
    sync.set_defaults(func=ds_sync)

    remove = subparsers.add_parser('remove', help='Remove files from the dataset')
    remove.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    remove.add_argument('--files', type=str, nargs='*',
                        help='Files / folders to remove (support for wildcard selection). '
                             'Notice: File path is the dataset path not the local path. '
                             'Example: data/*.jpg data/jsons/')
    remove.add_argument('--non-recursive', action='store_true', default=False,
                        help='Disable recursive scan of files')
    remove.add_argument('--verbose', action='store_true', default=False, help='Verbose reporting')
    remove.set_defaults(func=ds_remove_files)

    upload = subparsers.add_parser('upload', help='Upload the local dataset changes to the server')
    upload.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    upload.add_argument('--storage', type=str, default=None,
                        help='Remote storage to use for the dataset (default: files server). '
                             'Examples: \'s3://bucket/data\', \'gs://bucket/data\', \'azure://bucket/data\', '
                             '\'/mnt/shared/folder/data\'')
    upload.add_argument('--verbose', default=False, action='store_true', help='Verbose reporting')
    upload.set_defaults(func=ds_upload)

    finalize = subparsers.add_parser('close', help='Finalize and close the dataset (implies auto upload)')
    finalize.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    finalize.add_argument('--verbose', action='store_true', default=False, help='Verbose reporting')
    finalize.set_defaults(func=ds_close)

    delete = subparsers.add_parser('delete', help='Delete a dataset')
    delete.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    delete.add_argument('--force', action='store_true', default=False,
                        help='Force dataset deletion even if other dataset versions depend on it')
    delete.set_defaults(func=ds_delete)

    compare = subparsers.add_parser('compare', help='Compare two datasets (target vs source)')
    compare.add_argument('--source', type=str, required=True, help='Source dataset id (used as baseline)')
    compare.add_argument('--target', type=str, required=True,
                         help='Target dataset id (compare against the source baseline dataset)')
    compare.add_argument('--verbose', default=False, action='store_true',
                         help='Verbose report all file changes (instead of summary)')
    compare.set_defaults(func=ds_compare)

    squash = subparsers.add_parser('squash',
                                   help='Squash multiple datasets into a single dataset version (merge down)')
    squash.add_argument('--name', type=str, required=True, help='Creat squashed dataset name')
    squash.add_argument('--ids', type=str, required=True, nargs='*', help='Source dataset IDs to squash (merge down)')
    squash.add_argument('--storage', type=str, default=None, help='See `upload storage`')
    squash.add_argument('--verbose', default=False, action='store_true',
                        help='Verbose report all file changes (instead of summary)')
    squash.set_defaults(func=ds_squash)

    search = subparsers.add_parser('search', help='Search datasets in the system (sorted by creation time)')
    search.add_argument('--ids', type=str, nargs='*', help='Specify list of dataset IDs')
    search.add_argument('--project', type=str, help='Specify datasets project name')
    search.add_argument('--name', type=str, help='Specify datasets partial name matching')
    search.add_argument('--tags', type=str, nargs='*', help='Specify list of dataset user tags')
    search.set_defaults(func=ds_search)

    verify = subparsers.add_parser('verify', help='Verify local dataset content')
    verify.add_argument('--id', type=str, required=True, help='Specify dataset id')
    verify.add_argument('--folder', type=str,
                        help='Specify dataset local copy (if not provided the local cache folder will be verified)')
    verify.add_argument('--filesize', action='store_true', default=False,
                        help='If True, only verify file size and skip hash checks (default: false)')
    verify.add_argument('--verbose', action='store_true', default=False, help='Verbose reporting')
    verify.set_defaults(func=ds_verify)

    ls = subparsers.add_parser('list', help='List dataset content')
    ls.add_argument('--id', type=str, required=True, help='Specify dataset id (or use project/name instead)')
    ls.add_argument('--project', type=str, help='Specify dataset project name')
    ls.add_argument('--name', type=str, help='Specify dataset name')
    ls.add_argument('--filter', type=str, nargs='*',
                    help='Filter files based on folder / wildcard, multiple filters are supported. '
                         'Example: folder/date_*.json folder/sub-folder')
    ls.add_argument('--modified', action='store_true', default=False,
                    help='Only list file changes (add/remove/modify) introduced in this version')
    ls.set_defaults(func=ds_list)

    get = subparsers.add_parser('get', help='Get a local copy of a dataset (default: read only cached folder)')
    get.add_argument('--id', type=str, required=True, help='Previously created dataset id')
    get.add_argument('--copy', type=str, default=None,
                     help='Get a writable copy of the dataset to a specific output folder')
    get.add_argument('--link', type=str, default=None,
                     help='Create a soft link (not supported on Windows) to a '
                          'read-only cached folder containing the dataset')
    get.add_argument('--overwrite', action='store_true', default=False, help='If True, overwrite the target folder')
    get.add_argument('--verbose', action='store_true', default=False, help='Verbose reporting')
    get.set_defaults(func=ds_get)

    args = parser.parse_args()
    if args.command:
        try:
            args.func(args)
        except Exception as ex:
            print('Error: {}'.format(ex))
            return 1
    else:
        parser.print_help()


def ds_delete(args):
    print('Deleting dataset id={}'.format(args.id))
    print_args(args)
    Dataset.delete(dataset_id=args.id)
    print('Dataset {} deleted'.format(args.id))
    return 0


def ds_verify(args):
    print('Verify dataset id={}'.format(args.id))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    files_error = ds.verify_dataset_hash(
        local_copy_path=args.folder or None, skip_hash=args.filesize, verbose=args.verbose)
    if files_error:
        print('Dataset verification completed, {} errors found!'.format(len(files_error)))
    else:
        print('Dataset verification completed successfully, no errors found.')


def ds_get(args):
    print('Download dataset id={}'.format(args.id))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    if args.overwrite:
        if args.copy:
            # noinspection PyBroadException
            try:
                shutil.rmtree(args.copy)
            except Exception:
                pass
            Path(args.copy).mkdir(parents=True, exist_ok=True)
        elif args.link:
            # noinspection PyBroadException
            try:
                shutil.rmtree(args.link)
            except Exception:
                pass
    if args.copy:
        ds_folder = args.copy
        ds.get_mutable_local_copy(target_folder=ds_folder)
    else:
        if args.link:
            Path(args.link).mkdir(parents=True, exist_ok=True)
            # noinspection PyBroadException
            try:
                Path(args.link).rmdir()
            except Exception:
                try:
                    Path(args.link).unlink()
                except Exception:
                    raise ValueError("Target directory {} is not empty. Use --overwrite.".format(args.link))
        ds_folder = ds.get_local_copy()
        if args.link:
            os.symlink(ds_folder, args.link)
            ds_folder = args.link
    print('Dataset local copy available: {}'.format(ds_folder))
    return 0


def ds_list(args):
    print('List dataset content: {}'.format(args.id or (args.project, args.name)))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id or None, dataset_project=args.project or None, dataset_name=args.name or None)
    print('Listing dataset content')
    formatting = '{:64} | {:10} | {:64}'
    print(formatting.format('file name', 'size', 'hash'))
    print('-' * len(formatting.format('-', '-', '-')))
    filters = args.filter if args.filter else [None]
    file_entries = ds.file_entries_dict
    num_files = 0
    total_size = 0
    for mask in filters:
        files = ds.list_files(dataset_path=mask, dataset_id=ds.id if args.modified else None)
        num_files += len(files)
        for f in files:
            e = file_entries[f]
            print(formatting.format(e.relative_path, e.size, e.hash))
            total_size += e.size

    print('Total {} files, {} bytes'.format(num_files, total_size))
    return 0


def ds_squash(args):
    print('Squashing datasets ids={} into target dataset named \'{}\''.format(args.ids, args.name))
    print_args(args)
    ds = Dataset.squash(dataset_name=args.name, dataset_ids=args.ids, output_url=args.storage or None)
    print('Squashing completed, new dataset created id={}'.format(ds.id))
    return 0


def ds_search(args):
    def datetime_converter(o):
        if isinstance(o, datetime):
            return o.__str__()

    print('Search datasets')
    print_args(args)
    datasets = Dataset.list_datasets(
        dataset_project=args.project or None, partial_name=args.name or None,
        tags=args.tags or None, ids=args.ids or None
    )
    print(json.dumps(datasets, indent=4, default=datetime_converter))
    return 0


def ds_compare(args):
    print('Comparing target dataset id={} with source dataset id={}'.format(args.target, args.source))
    print_args(args)
    ds = Dataset.get(dataset_id=args.target)
    removed_files = ds.list_removed_files(dataset_id=args.source)
    modified_files = ds.list_modified_files(dataset_id=args.source)
    added_files = ds.list_added_files(dataset_id=args.source)
    if args.verbose:
        print('Removed files:')
        print('\n'.join(removed_files))
        print('\nModified files:')
        print('\n'.join(modified_files))
        print('\nAdded files:')
        print('\n'.join(added_files))
        print('')
    print('Comparison summary: {} files removed, {} files modified, {} files added'.format(
        len(removed_files), len(modified_files), len(added_files)))
    return 0


def ds_close(args):
    print('Finalizing dataset id={}'.format(args.id))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    ds.finalize()
    print('Dataset closed and finalized')
    return 0


def ds_upload(args):
    print('uploading local files to dataset id={}'.format(args.id))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    ds.upload(verbose=args.verbose, output_url=args.storage or None)
    print('Dataset upload completed')
    return 0


def ds_remove_files(args):
    print('Removing files/folder from dataset id={}'.format(args.id))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    num_files = 0
    for file in args.files:
        num_files += ds.remove_files(
            dataset_path=file,
            recursive=not args.non_recursive, verbose=args.verbose)
    print('{} files removed'.format(num_files))
    return 0


def ds_sync(args):
    print('Syncing dataset id={} to local folder {}'.format(args.id, args.folder))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    ds.sync_folder(local_path=args.folder, dataset_path=args.dataset_folder or None, verbose=args.verbose)
    print('Sync completed')
    return 0


def ds_add(args):
    print('Adding files/folder to dataset id={}'.format(args.id))
    print_args(args)
    ds = Dataset.get(dataset_id=args.id)
    num_files = 0
    for file in args.files:
        num_files += ds.add_files(
            path=file, recursive=not args.non_recursive,
            verbose=args.verbose, dataset_path=args.dataset_folder or None)
    print('{} files added'.format(num_files))
    return 0


def ds_create(args):
    print('Creating a new dataset:')
    print_args(args)
    ds = Dataset.create(dataset_project=args.project, dataset_name=args.name, parent_datasets=args.parents)
    if args.tags:
        ds.tags = ds.tags + args.tags
    print('New dataset created id={}'.format(ds.id))
    return 0


if __name__ == '__main__':
    exit(main())
