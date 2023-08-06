"""Official Python client for Driverless AI."""

import importlib
import json
import os
import re
from typing import Any
from typing import Callable
from typing import Optional
from typing import Union

import requests

from driverlessai import __version__
from driverlessai import _datasets
from driverlessai import _experiments
from driverlessai import _mli
from driverlessai import _projects
from driverlessai import _recipes
from driverlessai import _server
from driverlessai import _utils


###############################
# Custom Exceptions
###############################


# If we're not able to communicate with the DAI
# server, this exception is thrown.
class ServerDownException(_utils.ClientException):
    pass


# If we're not able to scrape server version
class ServerVersionExtractionFailed(_utils.ClientException):
    pass


class ServerVersionNotSupported(_utils.ClientException):
    pass


###############################
# Helper Functions
###############################


def is_server_up(
    address: str, timeout: int = 10, verify: Union[bool, str] = False
) -> bool:
    """Checks if a Driverless AI server is running.

    Args:
        address: full URL of the Driverless AI server to connect to
        timeout: timeout if the server has not issued a response in this many seconds
        verify: when using https on the Driverless AI server, setting this to
            False will disable SSL certificates verification. A path to
            cert(s) can also be passed to verify, see:
            https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification

    Examples::

        driverlessai.is_server_up(
            address='http://localhost:12345',
        )
    """
    try:
        return requests.get(address, timeout=timeout, verify=verify).status_code == 200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False


###############################
# DAI Python Client
###############################


class Client:
    """Connect to and interact with a Driverless AI server.

    Args:
        address: full URL of the Driverless AI server to connect to
        username: username for authentication on the Driverless AI server
        password: password for authentication on the Driverless AI server
        token_provider: callable that provides an authentication token,
            if provided, will ignore ``username`` and ``password`` values
        verify: when using https on the Driverless AI server, setting this to
            False will disable SSL certificates verification. A path to
            cert(s) can also be passed to verify, see:
            https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification
        backend_version_override: version of client backend to use, overrides
            Driverless AI server version detection. Specify ``"latest"`` to get
            the most recent backend supported. In most cases the user should
            rely on Driverless AI server version detection and leave this as
            the default ``None``.

    Attributes:
        connectors (Connectors): for interacting with connectors on the
            Driverless AI server
        datasets (Datasets): for interacting with datasets on the
            Driverless AI server
        experiments (Experiments): for interacting with experiments on the
            Driverless AI server
        mli (MLI): for interacting with experiment interpretations on the
            Driverless AI server
        projects (Projects): for interacting with projects on the
            Driverless AI server
        recipes (Recipes): for interacting with recipes on the
            Driverless AI server
        server (Server): for getting information about the Driverless AI server

    Examples::

        dai = driverlessai.Client(
            address='http://localhost:12345',
            username='py',
            password='py'
        )
    """

    def __init__(
        self,
        address: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token_provider: Optional[Callable[[], str]] = None,
        verify: Union[bool, str] = True,
        backend_version_override: Optional[str] = None,
    ) -> None:
        address = address.rstrip("/")

        # Check if the server is up, if we're unable to ping it we fail.
        if not is_server_up(address, verify=verify):
            if address.startswith("https"):
                raise ServerDownException(
                    "Unable to communicate with Driverless AI server. "
                    "Please make sure the server is running, "
                    "the address is correct, and `verify` is specified."
                )
            raise ServerDownException(
                "Unable to communicate with Driverless AI server. "
                "Please make sure the server is running and the address is correct."
            )

        # Try to get server version, if we can't we fail.
        if backend_version_override is None:
            server_version = self._detect_server_version(address, verify)
        else:
            if backend_version_override == "latest":
                backend_version_override = re.search("[0-9.]+", __version__)[0].rstrip(
                    "."
                )
            server_version = backend_version_override

        # Import backend that matches server version, if we can't we fail.
        server_module_path = (
            f"driverlessai._h2oai_client_{server_version.replace('.', '_')}"
        )
        try:
            self._server_module: Any = importlib.import_module(server_module_path)
        except ModuleNotFoundError:
            raise ServerVersionNotSupported(
                f"Server version {server_version} is not supported, "
                "try updating to the latest client."
            )

        self._backend = self._server_module.protocol.Client(
            address=address,
            username=username,
            password=password,
            token_provider=token_provider,
            verify=verify,
        )
        if server_version[:3] == "1.9":
            self._gui_sep = "/#/"
        if server_version[:3] == "1.8":
            self._gui_sep = "/#"
        self.connectors = _datasets.Connectors(self)
        self.datasets = _datasets.Datasets(self)
        self.experiments = _experiments.Experiments(self)
        self.mli = _mli.MLI(self)
        self.projects = _projects.Projects(self)
        self.recipes = _recipes.Recipes(self)
        self.server = _server.Server(
            self, address, username, self._backend.get_app_version().version
        )

        # Warns if license is missing/expired/about to expire
        self.server.license.is_valid()

    def __repr__(self) -> str:
        return f"{self.__class__} {self!s}"

    def __str__(self) -> str:
        return self.server.address

    @staticmethod
    def _detect_server_version(address: str, verify: Union[bool, str]) -> str:
        """Trys multiple methods to retrieve server version."""
        # query server version endpoint
        response = requests.get(f"{address}/serverversion", verify=verify)
        if response.status_code == 200:
            try:
                return response.json()["serverVersion"]
            except json.JSONDecodeError:
                pass
        # extract the version by scraping the login page
        response = requests.get(address, verify=verify)
        scrapings = re.search("DRIVERLESS AI ([0-9.]+)", response.text)
        if scrapings:
            return scrapings[1]
        # if login is disabled, get cookie and make rpc call
        with requests.Session() as s:
            s.get(f"{address}/login", verify=verify)
            response = s.post(
                f"{address}/rpc",
                data=json.dumps(
                    {"id": "", "method": "api_get_app_version", "params": {}}
                ),
            )
            try:
                return response.json()["result"]["version"]
            except json.JSONDecodeError:
                pass
        # fail
        raise ServerVersionExtractionFailed(
            "Unable to extract server version. "
            "Please make sure the address is correct."
        )

    def _download(
        self,
        server_path: str,
        dst_dir: str,
        dst_file: Optional[str] = None,
        overwrite: bool = False,
        timeout: float = 30,
        verbose: bool = True,
    ) -> str:
        if not dst_file:
            dst_file = os.path.basename(server_path)
        dst_path = os.path.join(dst_dir, dst_file)
        if overwrite or not os.path.exists(dst_path):
            url = self.server.address + "/files/" + server_path
            if hasattr(self._backend, "_session") and hasattr(
                self._backend, "_get_authorization_headers"
            ):
                res = self._backend._session.get(
                    url,
                    headers=self._backend._get_authorization_headers(),
                    timeout=timeout,
                )
            elif hasattr(self._backend, "_session"):
                res = self._backend._session.get(url, timeout=timeout)
            else:
                res = requests.get(
                    url,
                    cookies=self._backend._cookies,
                    verify=self._backend._verify,
                    timeout=timeout,
                )
            res.raise_for_status()
            with open(dst_path, "wb") as f:
                f.write(res.content)
        else:
            raise FileExistsError(
                dst_path + " already exists. Use `overwrite` to force download."
            )
        if verbose:
            print("Downloaded '", dst_path, "'", sep="")
        return dst_path
