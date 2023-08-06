import pytest
import requests
import requests_mock

from fasjson_client.client import Client
from fasjson_client import errors


def test_client_normalize_url(mocker):
    mocker.patch.object(Client, "_make_bravado_client")
    c = Client("http://localhost/fasjson")
    assert c._spec_url == "http://localhost/fasjson/specs/v1.json"


def test_client_wrong_url(mocker):
    mocker.patch("fasjson_client.client.GssapiAuthenticator", return_value=None)
    with requests_mock.mock() as m, pytest.raises(errors.ClientSetupError) as e:
        m.get("http://example.com/specs/v1.json", status_code=404, reason="Not Found")
        Client("http://example.com/")
    err = e.value
    expected_msg = (
        "error loading remote spec, are you sure this is the URL to a FASJSON instance?"
    )
    assert str(err) == expected_msg
    assert err.data["message"] == "404 Not Found"


def test_client_spec_parse_error(mocker):
    mocker.patch("fasjson_client.client.GssapiAuthenticator", return_value=None)
    with requests_mock.mock() as m, pytest.raises(errors.ClientSetupError) as e:
        m.get("http://example.com/specs/v1.json", text="{somethin: {wrong:")
        Client("http://example.com")
    err = e.value

    assert "remote data validation failed" == str(err)
    assert err.code == 71


def test_client_spec_invalid(mocker):
    mocker.patch("fasjson_client.client.GssapiAuthenticator", return_value=None)
    with requests_mock.mock() as m, pytest.raises(errors.ClientSetupError) as e:
        m.get("http://example.com/specs/v1.json", text='{"foo": "bar"}')
        Client("http://example.com")
    err = e.value

    assert "schema validation failed" == str(err)
    assert err.code == 71


def test_client_conn_error(mocker):
    mocker.patch("fasjson_client.client.GssapiAuthenticator", return_value=None)
    with requests_mock.mock() as m, pytest.raises(errors.ClientSetupError) as e:
        m.get(
            "http://example.com/specs/v1.json",
            exc=requests.exceptions.ConnectTimeout("A timeout occurred"),
        )
        Client("http://example.com")
    err = e.value

    expected_msg = (
        "error loading remote spec, are you sure this is the URL to a FASJSON instance?"
    )
    assert str(err) == expected_msg


def test_client_response_error(mocker):
    mocker.patch("fasjson_client.client.GssapiAuthenticator", return_value=None)
    with requests_mock.mock() as m, pytest.raises(errors.ClientSetupError) as e:
        m.get("http://example.com/specs/v1.json", reason="Forbidden", status_code=403)
        Client("http://example.com")
    err = e.value

    expected_msg = (
        "error loading remote spec, are you sure this is the URL to a FASJSON instance?"
    )
    assert str(err) == expected_msg
    assert err.data["status_code"] == 403
    assert err.data["message"] == "403 Forbidden"
