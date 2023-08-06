# pylint: disable=bad-option-value,too-many-branches,too-complex,too-many-locals,too-many-statements
"""
Data repo CLI module
"""
import argparse
import datetime
import os
import shutil
import tempfile
from distutils import dir_util
from typing import List

import yaml

from ..datarepo.mappers.csv_to_file import CSVToFileMapper
from ..datarepo.mappers.file_to_file import FileToFileMapper
from ..datarepo.storage.azure_blob import AzureBlobStorage
from ..datarepo.storage.storage_utils import generate_azure_account_sas

_CONFIG_FILE_DEFAULT_NAME = "datarepo.yml"
_DEFAULT_ERROR = 255


def _cli_main(parser: argparse.ArgumentParser, args_list: List[str]):
    """
    Runs MLDL CLI commands

    Args:
        parser (argparse.ArgumentParser): argument parser object
        args_list (List[str]): command line arguments
    """
    # datarepo.yaml contains a specific data repository configuration configuration
    # Expected configuration variables and example values:
    # data_azure_storage_container_uri: "https://storageaccountname.blob.core.windows.net/container_name"
    #   - data storage container uri
    # data_azure_storage_path: "folder/subfolder" - data storage path (under the container)
    # data_azure_storage_connection_string: "..."
    #       - connection string for the data storage account or a SAS-token 
    #         (SAS token should start with '?' or 'sas:')
    #
    # datarepo.yaml must be either in current directory or in .local directory next to this script

    args = parser.parse_args(args_list)

    do_list = False
    do_cache = False
    do_link = False
    with_storage = False
    use_temp_cache = False

    labels_dir = os.path.abspath(os.path.normpath(args.labels_dir))
    if not os.path.exists(labels_dir):
        print(f"Labels directory \"{labels_dir}\" does not exist")
        parser.exit(_DEFAULT_ERROR)

    if args.cache_dir is not None:
        cache_dir = os.path.abspath(os.path.normpath(args.cache_dir))
    else:
        cache_dir = None

    if "cache" in args.stage or "list" in args.stage:
        with_storage = True

    if with_storage:
        # Check config file
        if args.config_file is None:
            config_file = _CONFIG_FILE_DEFAULT_NAME
            if not os.path.exists(config_file):
                config_file = f".local/{_CONFIG_FILE_DEFAULT_NAME}"
                if not os.path.exists(config_file):
                    print(f"Cannot find {_CONFIG_FILE_DEFAULT_NAME}. "
                            "It must be either in the current directory "  # noqa: E127
                            "or in .local directory or "  # noqa: E127
                            "at a path provided with --config option.")  # noqa: E127
                    parser.exit(_DEFAULT_ERROR)
        else:
            config_file = args.config_file
            if not os.path.exists(config_file):
                print(f"{config_file} doesn't exist or not accessible.")
                parser.exit(_DEFAULT_ERROR)

        # parse config file
        with open(config_file) as cfg_file:
            config = yaml.safe_load(cfg_file)

        if "list" in args.stage:
            do_list = True
            if cache_dir is None:
                cache_dir = tempfile.mkdtemp()
                use_temp_cache = True
        else:
            if cache_dir is None:
                print("--cache value is required for caching.")
                parser.exit(_DEFAULT_ERROR)
            do_cache = True

        # configure storage
        os.makedirs(cache_dir, exist_ok=True)
        storage = AzureBlobStorage(cache_dir,
                                   config['data_azure_storage_container_uri'],
                                   config['data_azure_storage_path'] 
                                   if 'data_azure_storage_path' in config
                                        else None)

        storage_connection = ""
        if 'data_azure_storage_connection_string' in config:
            storage_connection = config['data_azure_storage_connection_string']
        elif args.storage_connection is not None:
            storage_connection = args.storage_connection

        if storage_connection is None or storage_connection == "":
            print("Storage connection string or a SAS-token must be provided in the configuration file "  # noqa: E127
                "or as --storage-connection option.")
            parser.exit(_DEFAULT_ERROR)

        # if storage_connection is an SAS-token, starts with '?'
        if storage_connection.startswith('?'):
            storage.authenticate(storage_connection[1:])
        # if storage_connection is an SAS-token, starts with 'sas:'
        elif storage_connection.casefold().startswith('sas:'):
            storage.authenticate(storage_connection[4:])
        # otherwise it's a connection string, and we generate an SAS token before authenticating
        else:
            storage.authenticate(generate_azure_account_sas(storage_connection))

    if not do_list and "link" in args.stage:
        if args.data_dir is None:
            print("--data value is required for linking")
            parser.exit(_DEFAULT_ERROR)

        do_link = True

    if not do_list:
        if args.labels_template is None:
            print("--labels_template value is required for file mapper")
            parser.exit(_DEFAULT_ERROR)
        elif args.labels_template.startswith("/"):
            args.labels_template = args.labels_template[1:]
        else:
            args.labels_template = f"**/*{args.labels_template}"

        if args.mapper_type == "file":
            if args.data_ext is None:
                print("--data_extension value is required for file mapper")
                parser.exit(_DEFAULT_ERROR)

            mapper = FileToFileMapper(
                cache_dir, labels_dir, args.labels_template, args.data_ext)
        elif args.mapper_type == "csv":
            mapper = CSVToFileMapper(
                cache_dir, labels_dir, args.labels_template, int(args.csv_col), not args.csv_use_header)

        files = mapper.map_files()
        total_len = len(files)
        print(f"Mapped {total_len} file entries.")
    else:
        # performing listing
        print(f"Listing storage in groups of {args.group_len} items.")
        storage.generate_storage_lists(int(args.group_len))
        print("Copying listing files")
        dir_util.copy_tree(cache_dir, labels_dir, preserve_mode=0, preserve_times=0)
        print(f"Done listing. Files are in {labels_dir}")

    if do_cache:
        print(f"Caching files to {cache_dir}.")
        start_time = datetime.datetime.now()
        storage.cache_items(files)
        end_time = datetime.datetime.now()
        print(f"Caching completed. Total time: {(end_time-start_time).total_seconds()} seconds.")

    if do_link:
        data_dir = os.path.abspath(os.path.normpath(args.data_dir))
        good_files = 0
        print(f"Caching files from {data_dir} to {cache_dir}.")

        for file in files:
            repo_file_path = os.path.abspath(os.path.join(data_dir, file))
            cached_path = storage.get_cached_path(file)
            if os.path.exists(cached_path):
                if os.path.exists(repo_file_path):
                    if os.path.islink(repo_file_path):
                        os.unlink(repo_file_path)
                    else:
                        os.remove(repo_file_path)
                dir_name = os.path.dirname(repo_file_path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                repo_file_dir = os.path.dirname(repo_file_path)
                cached_relative = os.path.relpath(cached_path, repo_file_dir)
                os.symlink(cached_relative, repo_file_path)
                good_files += 1
            else:
                print(f"File {repo_file_path} was not cached. Skipping.")

        print(f"Linking completed. {good_files} new links have been made.")

    if use_temp_cache:
        shutil.rmtree(cache_dir)


def _create_parser() -> argparse.ArgumentParser:
    """
    Creates command line parser for MLDL tool

    Returns:
        argparse.ArgumentParser: argument parser
    """
    parser = argparse.ArgumentParser(
        description='Machine Learning Data Lineage Tool')

    parser.add_argument('-s', '--stage', help='Stage.',
                        nargs='+', action='store', dest='stage', required=True,
                        choices=['list', 'cache', 'link'])

    parser.add_argument('-m', '--mapper', help='Labels to data mapper type. Required for cache and map stages.',
                        action='store', dest='mapper_type', required=False)

    parser.add_argument('--labels_template',
                        help="Labels file name template (e.g. \".json\" or \"/name.csv\"). "
                        "Forward slash means specific name. Without it, template resolves with '**/*' prefix.",
                        action='store', dest='labels_template', required=False)

    parser.add_argument('--data_extension', help='Data file extension (e.g. \".jpg\"). Only required for file mapper.',
                        action='store', dest='data_ext', required=False)

    parser.add_argument('--csv_column_index', help="Index of CSV column with file names. "
                        "First column index is 0 (default). Only used with csv mapper.",
                        action='store', dest='csv_col', default=0, required=False)

    parser.add_argument('--csv_no_header', help='Specify if CSV files do not have header line. Only used with csv mapper.',
                        action='store_false', dest='csv_use_header', default=False, required=False)

    parser.add_argument('-c', '--cache', help='Cache directory.',
                        action='store', dest='cache_dir', required=False)

    parser.add_argument('-l', '--labels', help='Labels directory.',
                        action='store', dest='labels_dir', required=True)

    parser.add_argument('-d', '--data', help='Data directory. Required for link stage.',
                        action='store', dest='data_dir', required=False)

    parser.add_argument('--group_len', help='Maximum number of files in a listing file. Required for list stage.',
                        action='store', dest='group_len', default=1000)

    parser.add_argument('--config', help='Configuration file. Required for cache and list stages.',
                        action='store', dest='config_file', required=False)
    
    parser.add_argument('--storage-connection', 
                        help='Storage connection string or SAS token. Used with cache and list stages when is not in the configuration file.',
                        action='store', dest='storage_connection', required=False)

    return parser


def main(args: List[str]):
    """
    Main function

    Args:
        args (List[str]): command line arguments
    """
    parser = _create_parser()
    _cli_main(parser, args)
