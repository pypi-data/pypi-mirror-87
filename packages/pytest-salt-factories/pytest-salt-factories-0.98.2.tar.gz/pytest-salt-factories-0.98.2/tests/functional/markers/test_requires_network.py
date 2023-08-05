"""
    tests.functional.markers.test_requires_network
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the ``@pytest.mark.requires_network`` marker
"""
import socket
from unittest import mock

from saltfactories.utils import ports


def test_has_local_network(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.requires_network
        def test_one():
            assert True
        """
    )
    res = testdir.runpytest()
    res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_no_local_network(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.requires_network
        def test_one():
            assert True
        """
    )
    mock_socket = mock.MagicMock()
    mock_socket.bind = mock.MagicMock(side_effect=socket.error)
    with mock.patch(
        "saltfactories.utils.ports.get_unused_localhost_port",
        side_effect=[ports.get_unused_localhost_port(), ports.get_unused_localhost_port()],
    ):
        with mock.patch("socket.socket", return_value=mock_socket):
            res = testdir.runpytest_inprocess("-p", "no:salt-factories-log-server")
            res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
