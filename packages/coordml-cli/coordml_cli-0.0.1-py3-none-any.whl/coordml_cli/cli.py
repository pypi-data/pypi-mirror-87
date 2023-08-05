import os.path as osp
from pathlib import Path
import argparse
import yaml
from coordml_cli.client import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_entry', type=str, help='CoordML Central API Endpoint.',
                        default='http://127.0.0.1:8888/api')
    subparsers = parser.add_subparsers(help='Actions', dest='action')
    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('config', type=str, help='Config path.')
    args = parser.parse_args()

    if args.action == 'create':
        config = yaml.load(open(args.config), yaml.Loader)
        exp_config = ExpConfig.from_yaml_config(config, str(Path(args.config).parent))
        client = CentralClient(args.api_entry)
        exp_id = client.create_exp(exp_config)
        print(f'Experiment created, id is {exp_id}')


if __name__ == '__main__':
    main()
