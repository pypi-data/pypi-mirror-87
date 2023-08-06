import os
import os.path

import yaml
from sdcclient import SdMonitorClient
from sdcclient import SdMonitorClient as SdMonitorClientV2
from sdcclient import SdSecureClient, SdScanningClient, SdSecureClientV1
from sdcclient.monitor import EventsClientV1
from sdcclient.secure import PolicyEventsClientOld

from sdccli.cli.formatter.json_formatter import JsonFormatter
from sdccli.cli.formatter.text_formatter import NormalFormatter


class Config(object):
    __default_config_paths = [
        os.path.expanduser("~") + "/.config/sdc-cli/config.yml",
        "/etc/sdc-cli/config.yml",
        "/config.yml"
    ]
    __default_monitor_url = 'https://app.sysdigcloud.com'
    __default_secure_url = 'https://secure.sysdig.com'

    def __init__(self, json=False):
        self.json = json
        self.formatter = JsonFormatter() if json else NormalFormatter()
        self.monitor = {}
        self.secure = {}

    def load(self, path=None, env=None):
        env = env if env is not None else os.getenv("SDC_ENV", "main")

        if path is None or path == "":
            found = False
            for file_path in self.__default_config_paths:
                if os.path.isfile(file_path):
                    path = file_path
                    found = True
            if not found:
                self.__config_with_defaults()
                return
        else:
            if not os.path.isfile(path):
                raise EnvironmentError("couldn't find the provided config file: {}".format(path))

        with open(path, "r") as f:
            try:
                config = yaml.load(f, Loader=yaml.SafeLoader)
            except yaml.YAMLError as exc:
                raise Exception("error in configuration file:", exc)

            if "envs" not in config:
                raise Exception("config file does not have a envs parent")

            if env not in config["envs"]:
                raise Exception("environment provided '{}' not found in the configuration file, "
                                "envs found: {}".format(env, list(config['envs'].keys())))

            self.__config_with_defaults(config["envs"][env])

    def __config_with_defaults(self, config=None):
        if config is None:
            config = {}

        monitor_token = os.environ.get('SDC_TOKEN')
        if os.environ.get('SDC_MONITOR_TOKEN'):
            monitor_token = os.environ.get('SDC_MONITOR_TOKEN')
        secure_token = os.environ.get('SDC_TOKEN')
        if os.environ.get('SDC_SECURE_TOKEN'):
            secure_token = os.environ.get('SDC_SECURE_TOKEN')

        monitor_url = self.__default_monitor_url
        if os.environ.get('SDC_MONITOR_URL'):
            monitor_url = os.environ.get('SDC_MONITOR_URL')
        secure_url = self.__default_secure_url
        if os.environ.get('SDC_SECURE_URL'):
            secure_url = os.environ.get('SDC_SECURE_URL')

        if 'monitor' in config:
            self.monitor = config["monitor"]
        if monitor_token:
            self.monitor['token'] = monitor_token
        if 'url' not in self.monitor:
            self.monitor['url'] = monitor_url
        self.monitor['ssl_verify'] = not self.monitor.get('disable_ssl_verification', False)

        if 'secure' in config:
            self.secure = config["secure"]
        if secure_token:
            self.secure['token'] = secure_token
        if 'url' not in self.secure:
            self.secure['url'] = secure_url
        self.secure['ssl_verify'] = not self.secure.get('disable_ssl_verification', False)

        self.monitor['url'] = self.monitor['url'].rstrip('/')
        self.secure['url'] = self.secure['url'].rstrip('/')

        if not (self.monitor['ssl_verify'] and self.secure['ssl_verify']):
            # suppress the InsecureRequestWarning when non tls connections are created
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @property
    def events_client_v1(self):
        return EventsClientV1(
            token=self.monitor["token"],
            sdc_url=self.monitor["url"],
            ssl_verify=self.monitor["ssl_verify"]
        )

    @property
    def sdmonitor(self):
        return SdMonitorClient(
            token=self.monitor["token"],
            sdc_url=self.monitor["url"],
            ssl_verify=self.monitor["ssl_verify"])

    @property
    def sdmonitor_v2(self):
        return SdMonitorClientV2(
            token=self.monitor["token"],
            sdc_url=self.monitor["url"],
            ssl_verify=self.monitor["ssl_verify"])

    @property
    def policy_events_client_old(self):
        return PolicyEventsClientOld(
            token=self.monitor["token"],
            sdc_url=self.monitor["url"],
            ssl_verify=self.monitor["ssl_verify"])

    @property
    def sdsecure(self):
        return SdSecureClient(
            token=self.secure["token"],
            sdc_url=self.secure["url"],
            ssl_verify=self.secure["ssl_verify"])

    @property
    def sdsecure_v1(self):
        return SdSecureClientV1(
            token=self.secure["token"],
            sdc_url=self.secure["url"],
            ssl_verify=self.secure["ssl_verify"])

    @property
    def sdscanning(self):
        return SdScanningClient(
            token=self.secure["token"],
            sdc_url=self.secure["url"],
            ssl_verify=self.secure["ssl_verify"])
