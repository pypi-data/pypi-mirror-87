"""
Module providing an interface for job driver implementations
"""

from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Any, Dict

from rocinante.config import RocinanteConfiguration


class Driver(metaclass=ABCMeta):
    """
    Abstract class for job drivers, that is, classes that manage incoming jobs

    Drivers must handle 3 things:
    - Extracting incoming data to obtain a job info
    - Obtaining the moulinette (including managing a cache if possible)
    - Formatting job results so they can be sent back
    """

    @staticmethod
    @abstractmethod
    def create(logger: Logger, root_directory: str, config: RocinanteConfiguration) -> 'Driver':
        """
        Create a Driver instance

        :param logger:          a logger through which the driver log information
        :param root_directory:  the directory to use as root for the driver
        :param config:          the configuration
        :return:                a properly-configured driver instance
        """
        pass

    @abstractmethod
    def extract_job_information(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract job information from the job body

        :param body:            the job body, as received from the message broker
        :return:                the extracted job information

        :raise:                 ValueError if the body is ill-formed
        """
        pass

    @abstractmethod
    def retrieve_moulinette(self, info: Dict[str, Any]) -> str:
        """
        Retrieve the moulinette and return a path to its directory
        Depending on its implementation, a driver can generate, download or copy moulinettes.

        :param info:            the job information
        :return:                the path to the moulinette directory

        :raise:                 any exception if the moulinette cannot be retrieved
        """
        pass

    @abstractmethod
    def format_result(self, body: Dict[str, Any], job_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the result of a job so that it can be sent back

        :param body:            the job body, as received from the message broker
        :param job_feedback:    the job feedback, as returned by Panza
        :return:                a dictionary containing the formatted data

        :raise:                 ValueError if the feedback and / or the body are ill-formed
        """
        pass
