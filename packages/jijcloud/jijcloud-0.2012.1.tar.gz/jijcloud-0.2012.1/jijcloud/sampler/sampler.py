import os
import dimod
from typing import Union
from jijcloud.post_api import post_instance_and_query
from jijcloud.setting import load_config
from jijcloud.config.handle_config import CONFIG_PATH, DEFAULT_CONFIG_FILE


class UrlPattern:
    def __init__(self, url: Union[str, dict]):
        if isinstance(url, dict):
            self.instance_url = url['instance_url']
            self.solver_url = url['solver_url']
        elif isinstance(url, str):
            self.instance_url, self.solver_url = url, url
        else:
            raise ValueError('needs url in config file')


class JijCloudSampler(dimod.Sampler):
    """JijCloudSampler
    another Sampler is based on this class
    """

    hardware = ''
    algorithm = ''

    def __init__(self, token: str=None, url: Union[str, dict]=None, timeout=None, config=None, config_env='default'):
        """setting token and url

        Args:
            token (str, optional): token string. Defaults to None.
            url (Union[str, dict], optional): API URL. Defaults to None.
            timeout (float, optional): timeout for post request. Defaults to None.
            config (str, optional): Config file path. Defaults to None.

        Raises:
            TypeError: token, url, config is not str
        """

        if isinstance(config, str):
            _config = load_config(config)[config_env]
            self.token = _config['token']
            if 'url' in _config:
                self.url = UrlPattern(_config['url'])
            else:
                self.url = UrlPattern({k: _config[k] for k in ['instance_url', 'solver_url']})
            self.timeout = _config.get('timeout', 1)
        elif isinstance(token, str) and isinstance(url, (type(None), str, dict)):
            self.token = token
            if not url:
                # default url
                self.url = UrlPattern('default url')
            else:
                self.url = UrlPattern(url)
        else:
            # Load default config file
            config = CONFIG_PATH + DEFAULT_CONFIG_FILE
            if not os.path.exists(config):
                raise ValueError('need config file or token and url')
            _config = load_config(config)[config_env]
            self.token = _config['token']
            if 'url' in _config:
                self.url = UrlPattern(_config['url'])
            else:
                self.url = UrlPattern({k: _config[k] for k in ['instance_url', 'solver_url']})


        self.timeout = timeout if timeout is not None else 1
       

    def sample(self, bqm, num_reads=1, num_sweeps=100, timeout=None, sync=True, **kwargs):
        parameters = {'num_reads': num_reads, 'num_sweeps': num_sweeps}
        parameters.update(kwargs)
        # if timeout is defined in script, use this value
        if timeout:
            self.timeout = timeout

        instance = {
            'instance_type': 'BQM',
            'instance': bqm.to_serializable()
        }
        solve_req = {
            'solver': self.algorithm,
            'parameters': parameters
        }
        response = post_instance_and_query(self.url.instance_url, self.url.solver_url, self.token, instance=instance, parameters=solve_req, sync=sync)
        return response

    @property
    def properties(self):
        return dict()

    @property
    def parameters(self):
        return dict()
