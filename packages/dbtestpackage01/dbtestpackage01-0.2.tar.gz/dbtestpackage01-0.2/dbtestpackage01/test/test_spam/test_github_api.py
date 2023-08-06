from unittest.mock import Mock

import pytest

from dbtestpackage01 import github_api


@pytest.fixture
def avatar_url(mocker):
    url = 'https://avatars2.githubusercontent.com/u/73870305?v=4'
    resp_mock = Mock()
    resp_mock.json.return_value = {
        'avatar_url': 'https://avatars2.githubusercontent.com/u/73870305?v=4'
    }
    get_mock = mocker.patch('dbtestpackage01.github_api.requests.get')
    get_mock.return_value = resp_mock
    return url


def test_github_api(avatar_url):
    url = github_api.buscar_avatar('boybluepiano')
    assert avatar_url == url


def test_github_integrado():
    url = github_api.buscar_avatar('boybluepiano')
    assert 'https://avatars2.githubusercontent.com/u/73870305?v=4' == url
