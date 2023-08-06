"""Client configuration"""
from typing import (
    Optional, Mapping, MutableMapping, Any
)
import os
import re
from pathlib import Path
from getpass import getpass
import json
import logging
import httpx
from appdirs import user_config_dir
from .auth import (
    WaylayCredentials,
    ClientCredentials, ApplicationCredentials, TokenCredentials, NoCredentials,
    WaylayTokenAuth, WaylayToken,
    parse_credentials,
    DEFAULT_ACCOUNTS_URL
)
from .exceptions import AuthError, ConfigError

log = logging.getLogger(__name__)

# http client dependencies
_http = httpx

TenantSettings = Mapping[str, str]
Settings = MutableMapping[str, str]

DEFAULT_PROFILE = '_default_'
SERVICE_KEY_API = 'waylay_api'


def tell(message: str):
    """interactive authentication message"""
    print(message)


def ask(prompt: str, secret: bool = False) -> str:
    """prompt user for credential information"""
    if secret:
        return getpass(prompt=prompt)
    else:
        return input(prompt)


class WaylayConfig():
    """Manages the authentication and endpoint configuration for the Waylay Platform"""
    profile: str
    settings_overrides: Settings
    credentials: WaylayCredentials
    _auth: _http.Auth
    _resolved_settings: Optional[TenantSettings] = None

    def __init__(
        self, credentials: WaylayCredentials = None, profile: str = DEFAULT_PROFILE,
        settings: TenantSettings = None, fetch_tenant_settings=True,
        auth: WaylayTokenAuth = None
    ):
        self.profile = profile
        if credentials is None:
            credentials = NoCredentials()
        self.credentials = credentials
        self.settings_overrides = dict(settings) if settings is not None else {}
        if auth is None:
            auth = WaylayTokenAuth(credentials, interactive=self.interactive)
        self._auth = auth
        if not fetch_tenant_settings:
            self._resolved_settings = {}

    def get_root_url(
        self, config_key: str, default_root_url: str = None, local=False
    ) -> Optional[str]:
        """get the root url for a waylay service"""
        config_key = _root_url_key_for(config_key)
        if default_root_url is None and config_key == SERVICE_KEY_API:
            default_root_url = _root_url_for(self.get_valid_token().domain)
        settings = self._local_settings if local else self.settings
        url = settings.get(config_key, default_root_url)
        if url is not None:
            return _root_url_for(url)
        return None

    def set_root_url(self, config_key: str, root_url: Optional[str]):
        """
        Overrides the root url for the given server (will persist on 'save').
        Setting a None value will remove the override.
        """
        config_key = _root_url_key_for(config_key)
        if root_url is None and config_key in self.settings_overrides:
            del self.settings_overrides[config_key]
        if root_url is not None:
            self.settings_overrides[config_key] = root_url

    @property
    def accounts_url(self):
        """accounts url (normalised)"""
        return _root_url_for(self.credentials.accounts_url)

    def interactive(self) -> WaylayCredentials:
        """ask interactively for credentials"""

        tell("Authenticating to the Waylay Platform")

        accounts_url = self.accounts_url
        acc_validated = False
        while not acc_validated:
            tell(f'Using authentication provider at [{accounts_url}]')
            accounts_url = ask(
                '> alternative endpoint (press enter to continue)?: '
            ) or accounts_url
            accounts_url = _root_url_for(accounts_url)
            accounts_status_resp = httpx.get(accounts_url)
            acc_validated = not accounts_status_resp.is_error
            if acc_validated:
                tell(f"Authenticating at '{accounts_status_resp.json()['name']}'")
            else:
                tell(f"Cannot connect to '{accounts_url}': {accounts_status_resp.reason_phrase}")

        tell("Please provide client credentials for the waylay data client.")
        credentials = ClientCredentials(api_key='', api_secret='', accounts_url=accounts_url)
        retry = 0
        while not credentials.is_well_formed() and retry < 3:
            api_key = ask(prompt='> apiKey : ', secret=False).strip()
            api_secret = ask(prompt='> apiSecret : ', secret=True).strip()
            credentials = ClientCredentials(
                api_key=api_key, api_secret=api_secret, accounts_url=accounts_url
            )
            if not credentials.is_well_formed():
                retry += 1
                if retry >= 3:
                    tell('Too many attempts, failing authentication')
                    raise AuthError('Too many attempts, failing authentication')
                tell('Invalid apiKey or apiSecret, please retry')
        self.credentials = credentials
        store = ''
        while not store or store[0].lower() not in ('n', 'y', 't', 'f'):
            store = ask(
                f'> Do you want to store these credentials (profile={self.profile})? [Y]: '
            ) or 'Y'
        if store[0].lower() in ('y', 't'):
            self.save()
            tell(
                f"Credential configuration stored as \n\t{self.config_file_path(self.profile)}\n"
                "Please make sure this file is treated securely.\n"
                "If compromised, _Revoke_ the api-key on the Waylay Console!"
            )
        return self.credentials

    @property
    def tenant_settings(self) -> TenantSettings:
        """
        Tenant settings as stored on accounts.
        Will fetch settings when not present and initialised with 'fetch_tenant_settings=True'.
        """
        if self._resolved_settings is None:
            self._resolved_settings = self._request_settings()

        return self._resolved_settings

    @property
    def settings(self) -> TenantSettings:
        """
        The tenant settings, as resolved form the accounts backend,
        and overridden with client config settings
        """
        return {
            **self.tenant_settings,
            **self.settings_overrides
        }

    @property
    def _local_settings(self) -> TenantSettings:
        """
        The locally available settings, including resolved settings
        from the backend if already present.
        """
        return {
            **(self._resolved_settings or {}),
            **self.settings_overrides
        }

    def get_valid_token(self) -> WaylayToken:
        """get the current valid authentication token or fail"""
        if isinstance(self.auth, WaylayTokenAuth):
            try:
                return self.auth.assure_valid_token()
            except AuthError as exc:
                raise ConfigError(f'cannot get valid token') from exc
        raise ConfigError('not using token authentication')

    @property
    def auth(self) -> _http.Auth:
        """returns the http authentication interceptor"""
        return self._auth

    @property
    def domain(self) -> Optional[str]:
        """the domain of the current user"""
        try:
            return self.get_valid_token().domain
        except ConfigError:
            return None

    def _request_settings(self) -> TenantSettings:
        try:
            settings_url = f"{self.get_root_url('api', local=True)}/api/settings"
            settings_resp = _http.get(settings_url, auth=self.auth)
            settings_resp.raise_for_status()
            return {
                key: value
                for key, value in settings_resp.json().items()
                if key.startswith('waylay_')
            }
        except _http.HTTPStatusError as exc:
            if exc.response.status_code == 403:
                log.warning(
                    "You are not authorised to fetch tenant settings.\n"
                    "The Waylay SAAS defaults will be used, unless you\n"
                    "provide explicit overrides in the SDK Configuration profile."
                )
                return {}
            raise ConfigError('cannot resolve tenant settings') from exc
        except _http.HTTPError as exc:
            raise ConfigError('cannot resolve tenant settings') from exc

    # config persistency methods
    @classmethod
    def config_file_path(cls, profile: str = DEFAULT_PROFILE) -> str:
        return os.path.join(user_config_dir('Waylay'), 'python_sdk', f".profile.{profile}.json")

    @classmethod
    def load(
        cls,
        profile: str = DEFAULT_PROFILE,
        interactive: bool = True,
        accounts_url: str = DEFAULT_ACCOUNTS_URL
    ):
        """load a stored waylay configuration"""
        try:
            with open(cls.config_file_path(profile), mode='r') as config_file:
                config_json = json.load(config_file)
            return cls.from_dict(config_json)
        except FileNotFoundError as exc:
            if not interactive:
                raise ConfigError(f'Config profile {profile} not found') from exc
            instance = cls(NoCredentials(accounts_url=accounts_url), profile=profile)
            return instance

    @classmethod
    def from_dict(cls, config_json: Mapping[str, Any]):
        config_json = dict(config_json)
        if 'credentials' in config_json:
            config_json['credentials'] = parse_credentials(config_json['credentials'])
        return cls(**config_json)

    def to_dict(self, obfuscate=True):
        return {
            'credentials': self.credentials.to_dict(obfuscate),
            'profile': self.profile,
            'settings': self.settings_overrides
        }

    def save(self):
        config_path = Path(self.config_file_path(self.profile))
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, mode='w') as config_file:
            json.dump(self.to_dict(obfuscate=False), config_file)
            log.info("wrote waylay configuration: %s", config_path)

    @classmethod
    def delete(cls, profile: str = DEFAULT_PROFILE):
        """delete a stored profile"""
        config_path = Path(cls.config_file_path(profile))
        if config_path.exists():
            config_path.unlink()
            log.warning("waylay configuration removed: %s", config_path)
        else:
            log.warning("waylay configuration not found: %s", config_path)

    @classmethod
    def list_profiles(cls):
        """list stored profiles"""
        config_dir = Path(cls.config_file_path()).parent
        return {
            re.match(r'\.profile\.(.*)\.json', config_file.name)[1]: str(config_file)
            for config_file in config_dir.iterdir()
        }

    def __repr__(self):
        return f'<WaylayConfig({str(self)})>'

    def __str__(self):
        return json.dumps(self.to_dict(obfuscate=True))


def _root_url_key_for(config_key: Optional[str] = None):
    if config_key is None:
        return SERVICE_KEY_API
    if config_key.startswith('waylay_'):
        return config_key
    return f"waylay_{config_key}"


def _root_url_for(config_value: Optional[str]) -> Optional[str]:
    """make sure any host name is converted in a https:// url"""
    if config_value and '://' not in config_value:
        return f'https://{config_value}'
    return config_value
