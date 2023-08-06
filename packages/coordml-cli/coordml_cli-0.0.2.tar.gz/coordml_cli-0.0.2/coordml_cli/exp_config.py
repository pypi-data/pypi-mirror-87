from collections import namedtuple
import os
import os.path as osp
import json

ResultView = namedtuple('ResultView', ['row_key', 'column_key'])


class ExpConfig:
    def __init__(self, title: str, author: str, config: dict, resolver_path: str, env_path: str, result_parse: str,
                 result_view: ResultView):
        self.title = title
        self.author = author
        self.config = config
        self.resolver_path = resolver_path
        self.env_path = env_path
        self.result_parse = result_parse
        self.result_view = result_view

    @staticmethod
    def from_yaml_config(obj: dict, yaml_path: str):
        os.chdir(yaml_path)
        return ExpConfig(
            title=obj['title'],
            author=obj['author'],
            config=obj['config'],
            resolver_path=osp.abspath(osp.expanduser(obj['resolver_path'])),
            env_path=osp.abspath(osp.expanduser(obj['env_path'])),
            result_parse=obj['result_parse'],
            result_view=ResultView(obj['result_view']['row_key'], obj['result_view']['column_key'])
        )

    def dump(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'config': self.config,
            'resolverPath': self.resolver_path,
            'envPath': self.env_path,
            'resultParse': self.result_parse,
            'resultView': {
                'rowKey': self.result_view.row_key,
                'columnKey': self.result_view.column_key
            }
        }
