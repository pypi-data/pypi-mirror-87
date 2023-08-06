"""Server module of official Python client for Driverless AI."""

import urllib.parse
from typing import Any

from driverlessai import _core
from driverlessai import _utils


class License:
    """Get information about the Driverless AI server's license."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def _get_info(self) -> Any:
        info = self._client._backend.have_valid_license()
        if info.message:
            print(info.message)
        return info

    def days_left(self) -> int:
        """Return days left on license.

        Examples::

            dai.server.license.days_left()
        """
        return self._get_info().days_left

    def is_valid(self) -> bool:
        """Return ``True`` if server is licensed.

        Examples::

            dai.server.license.is_valid()
        """
        return self._get_info().is_valid


class Server:
    """Get information about the Driverless AI server.

    Attributes:
        address (str): URL of the Driverless AI server connected to
        license (License): for getting information about the license on the
            Driverless AI server
        username (str): current user connected as to a Driverless AI server
        version (str): version of Driverless AI server currently connected to

    Examples::

        # Connect to the DAI server
        dai = driverlessai.Client(
            address='http://localhost:12345',
            username='py',
            password='py'
        )

        dai.server.address
        dai.server.username
        dai.server.version
    """

    def __init__(
        self, client: "_core.Client", address: str, username: str, version: str
    ) -> None:
        self._client = client
        self.address = address
        self.license = License(client)
        self.username = username
        self.version = version

    def docs(self, search: str = None) -> _utils.GUILink:
        """Get link to documentation on the Driverless AI server.

        Args:
            search: if search terms are supplied, the link will go to
                documentation search results

        Example::

            # Search the DAI docs for "licenses"
            dai.server.docs(search='licenses')
        """
        if search is None:
            return _utils.GUILink(f"{self.address}/docs/userguide/index.html")
        else:
            search = urllib.parse.quote_plus(search)
            link = f"{self.address}/docs/userguide/search.html?q={search}"
            return _utils.GUILink(link)

    def gui(self) -> _utils.GUILink:
        """Get full URL for the Driverless AI server.

        Examples::

            dai.server.gui()
        """
        return _utils.GUILink(self.address)
