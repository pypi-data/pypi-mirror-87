import pytest
import socket

from seeq import spy
from seeq.sdk import Configuration, UserOutputV1

from . import test_common

from .. import _config, _login


@pytest.mark.system
def test_bad_login():
    test_common.login()

    Configuration().retry_timeout_in_seconds = 0

    with pytest.raises(RuntimeError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', url='https://bogus')

    assert spy.client is None
    assert spy.user is None

    # Remove overrides that resulted from spy.login() with bogus URL
    _config.unset_seeq_url()

    with pytest.raises(ValueError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', auth_provider='bogus')

    assert spy.client is None
    assert spy.user is None


@pytest.mark.system
def test_good_login():
    test_common.login()

    assert spy.client is not None
    assert isinstance(spy.user, UserOutputV1)
    assert spy.user.username == 'agent_api_key'
    assert _config.Setting.SEEQ_URL.get() is None      # Should not be set, since we're using the default

    # force=False will mean that we don't try to login since we're already logged in
    spy.login(username='blah', password='wrong', force=False)

    assert spy.client is not None
    assert isinstance(spy.user, UserOutputV1)
    assert spy.user.username == 'agent_api_key'
    assert _config.Setting.SEEQ_URL.get() is None

    auth_token = spy.client.auth_token
    _login.client = None
    spy.client = None

    # Data Lab uses this pattern, and so we have to support it. We use gethostname() here just to make sure that the
    # default of http://localhost:34216 is not being used.
    url = f'http://{socket.gethostname()}:34216'
    spy._config.set_seeq_url(url)
    spy.login(auth_token=auth_token)

    assert spy.client is not None
    assert isinstance(spy.user, UserOutputV1)
    assert spy.user.username == 'agent_api_key'
    assert _config.Setting.SEEQ_URL.get() == url

    # Make sure we can do a simple search
    df = spy.search({'Name': 'Area A_Temperature'})
    assert len(df) > 0


@pytest.mark.system
def test_credentials_file_with_username():
    with pytest.raises(ValueError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', credentials_file='credentials.key')
