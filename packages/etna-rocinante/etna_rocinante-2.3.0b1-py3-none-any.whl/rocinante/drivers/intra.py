"""
Module implementing a driver for jobs issued by the intra
"""

import json
from logging import Logger
import os
from typing import Any, Dict

from etna_api import EtnaSession, EtnaAPIError
from panza.cache import Cache
from quixote.inspection import Scope

from rocinante.config import RocinanteConfiguration
from rocinante.errors import RetryableError
from rocinante.driver import Driver
from rocinante.utils import sanitize_for_filename, sanitize_for_environment_name


def _identify_job(info: Dict[str, Any]) -> str:
    if "stage" in info:
        return f"{info['module_id']}-{info['activity_id']}-{sanitize_for_filename(info['stage'])}-{info['group_id']}"
    else:
        return f"{info['module_id']}-{info['activity_id']}-{info['group_id']}"


def _identify_job_environment(info: Dict[str, Any]) -> str:
    if "stage" in info:
        return f"{info['module_id']}-{info['activity_id']}-{sanitize_for_environment_name(info['stage'])}"
    else:
        return f"{info['module_id']}-{info['activity_id']}"


def _failed_req_pretty_output(scope, indent=0):
    for entry in scope.entries:
        if isinstance(entry, Scope):
            sub_entries = [e for e in _failed_req_pretty_output(entry, indent + 2 * (not entry.hidden))]
            if sub_entries:
                if entry.hidden is False:
                    yield " " * indent + entry.name
                for sub_entry in sub_entries:
                    yield sub_entry
        else:
            assert isinstance(entry, dict)
            if "requirements" in entry:
                ok, req = entry["requirements"]
                if not ok:
                    yield " " * indent + "requirement failed: " + str(req)
            elif "assertion_failure" in entry:
                yield " " * indent + "assertion failed: " + entry["assertion_failure"]


class IntraValidationDriver(Driver):
    def __init__(self, logger: Logger, root_dir: str, config: RocinanteConfiguration):
        self.logger = logger
        self.cache = Cache.from_directory(root_dir, max_entries=64)
        self.root_dir = root_dir
        self.config = config

    @staticmethod
    def create(logger: Logger, root_directory: str, config: RocinanteConfiguration) -> 'Driver':
        return IntraValidationDriver(logger, root_directory, config)

    def extract_job_information(self, body: Dict[str, Any]) -> Dict[str, Any]:
        credentials = self.config.credentials["intra"]

        try:
            session = EtnaSession(
                username=credentials.username,
                password=credentials.password,
                request_retries=10,
                retry_on_statuses=(500, 502, 504)
            )

            info = {}
            _, module_id, _, activity_id = body["files_path"].split("/")
            info["module_id"] = int(module_id)
            info["activity_id"] = int(activity_id)
            info["module_name"] = session.get_module_by_id(info["module_id"])["uv_name"]
            info["activity_name"] = session.get_activity_by_id(info["module_id"], info["activity_id"])["name"]
            info["group_id"] = body["result"]["group_id"]
            info["leader"] = body["result"]["leader"]
            info["stage"] = body["result"]["stage"]
            info["stage_end"] = body["tokens"]["stage_end"]
            info["request_date"] = body["date"]
            info["job_name"] = _identify_job(info)
            info["job_environment"] = _identify_job_environment(info)
            info["dry_run"] = body["result"]["dry_run"]

        except EtnaAPIError as e:
            raise RetryableError(e)

        return info

    def _download_from_intra(self, moulinette_name: str, info: Dict[str, Any]):
        credentials = self.config.credentials["intra"]
        session = EtnaSession(
            username=credentials.username,
            password=credentials.password,
            request_retries=10,
            retry_on_statuses=(500, 502, 504)
        )

        intra_moulinette_dir = "resources/moulinette/"
        files = session.get_activity_stage_files_list(info["module_id"], info["activity_id"], info["stage"])

        files = map(lambda x: (x["rel_path"], x["rel_path"].rsplit(f"/stages/{info['stage']}/", maxsplit=1)[1]), files)
        files = filter(lambda x: x[1].startswith(intra_moulinette_dir), files)

        with self.cache.add_entry(moulinette_name) as entry_path:
            for dist_path, local in files:
                local = os.path.relpath(local, intra_moulinette_dir)
                dirname = os.path.dirname(local)
                if not os.path.exists(f"{entry_path}/{dirname}"):
                    os.makedirs(f"{entry_path}/{dirname}")
                data = session.download_file_from_activity(info["module_id"], info["activity_id"], dist_path)
                with open(f"{entry_path}/{local}", "wb") as f:
                    f.write(data)

    def retrieve_moulinette(self, info: Dict[str, Any]) -> str:
        sanitized_req_date = sanitize_for_filename(info["request_date"])
        moulinette_name = f"{_identify_job_environment(info)}-{sanitized_req_date}"

        if self.cache.has_entry(moulinette_name):
            self.logger.info(f"Reusing cached moulinette from {info['request_date']}")
            return self.cache.get_entry(moulinette_name)
        try:
            self.logger.info("Downloading the moulinette from the intranet...")
            try:
                self._download_from_intra(moulinette_name, info)
            except EtnaAPIError as e:
                raise RetryableError(e)
        except Exception:
            self.cache.remove_entry(moulinette_name)
            raise

        return self.cache.get_entry(moulinette_name)

    def format_result(self, body: Dict[str, Any], job_feedback: Dict[str, Any]) -> Dict[str, Any]:
        job_result = job_feedback["result"]
        failed_reqs = list(iter(_failed_req_pretty_output(job_result)))

        result_template = body["result"]
        if len(failed_reqs) > 0:
            result_template["output"] = "KO:\n" + "\n".join(failed_reqs)
            result_template["status"] = 1
        else:
            result_template["output"] = "OK"
            result_template["status"] = 0
        self.logger.info(f"Result status: {'KO' if result_template['status'] else 'OK'}")
        self.logger.info(f"Result feedback (as seen by students): {json.dumps(result_template['output'])}")
        return result_template
