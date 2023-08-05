import requests
from coordml_cli.exp_config import *


class CentralClient:
    def __init__(self, api_entry: str):
        self.api_entry = api_entry

    def create_exp(self, exp_config: ExpConfig):
        req = requests.post(f'{self.api_entry}/exp/create', json=exp_config.dump())
        return req.json()['expId']
