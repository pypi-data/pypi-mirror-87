
from waylay import WaylayConfig, ClientCredentials

from waylay.auth import WaylayTokenAuth, WaylayToken

def test_empty_config():
    cfg = WaylayConfig()
    assert isinstance(cfg.auth, WaylayTokenAuth)
    assert cfg.settings_overrides == {}
    # assert cfg.tenant_settings is None
    # assert cfg.settings == {}
    # assert cfg.get_root_url('a_service') == None
    
def test_create_config_credentials(mocker):
    pass
    # mock_get = mocker.patch('httpx.get')
    # cred = ClientCredentials('mykey', 'mysecret', accounts_url='http://localhost:9999')
    # cfg = WaylayConfig(cred)
    # assert isinstance(cfg.auth, WaylayTokenAuth)
    # assert cfg.settings_overrides == {}
    # assert cfg.tenant_settings is None
    # assert cfg.settings == {}
    # assert cfg.get_root_url('a_service','') == ''

def test_resolve_settings():
    pass

def test_settings_override():
    pass

def test_create_config():
    pass

def test_store_load_config_default():
    pass

def test_store_load_config_profile():
    pass

def test_store_load_config_setting_override():
    pass