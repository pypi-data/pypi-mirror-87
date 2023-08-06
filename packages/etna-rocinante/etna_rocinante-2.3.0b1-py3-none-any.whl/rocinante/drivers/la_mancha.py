import os
from logging import Logger
from typing import Dict, Any

from panza.cache import Cache
import requests

from rocinante.utils import sanitize_for_filename, sanitize_for_environment_name
from rocinante.driver import Driver
from rocinante.config import RocinanteConfiguration


class LaManchaDriver(Driver):
    def __init__(self, logger: Logger, root_dir: str, config: RocinanteConfiguration):
        self.logger = logger
        self.cache = Cache.from_directory(root_dir, max_entries=64) # not used yet
        self.root_dir = root_dir
        self.config = config

    @staticmethod
    def create(logger: Logger, root_directory: str, config: RocinanteConfiguration) -> 'Driver':
        return LaManchaDriver(logger, root_directory, config)

    def extract_job_information(self, body: Dict[str, Any]) -> Dict[str, Any]:
        info = {
            "inputs": body["inputs"],
            "request_date": body["request_date"],
            "blueprint_url": body["blueprint_url"],
            "job_name": f'{sanitize_for_filename(body["blueprint_url"])}-{sanitize_for_filename(body["title"])}-{sanitize_for_filename(body["request_date"])}',
            "job_environment": f'{sanitize_for_environment_name(body["blueprint_url"])}'
        }

        return info

    def retrieve_moulinette(self, info: Dict[str, Any]) -> str:
        response = requests.get(info["blueprint_url"], headers={"LaManchaAPIKey": self.config.credentials["la-mancha"].token})
        if response.status_code != 200:
            raise ValueError(f"Unexpected status code: {response.status_code} when requesting '{info['blueprint_url']}', got body: '{response.text}'")

        blueprint = response.text

        os.makedirs(f"{self.root_dir}/moulinette/", exist_ok=True)
        with open(f"{self.root_dir}/moulinette/blueprint.py", 'w') as blueprint_file:
            blueprint_file.write(blueprint)

        return f"{self.root_dir}/moulinette"

    def format_result(self, body: Dict[str, Any], job_feedback: Dict[str, Any]) -> Dict[str, Any]:
        results = [{}]
        for entry in job_feedback["result"].entries:
            if isinstance(entry, dict):
                if "results" in entry:
                    results = entry["results"]

        result_template = {
            "exports": body["exports"],
            "request_date": body["request_date"],
            "results": results,
            "title": body["title"],
        }

        return result_template
