from rest_framework import exceptions
import collections.abc


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class Config:
    required = ['email', 'name', 'phone']

    def __init__(self, config: dict):
        self.config = config

    def check_config(self, config):
        for field in self.required:
            if field not in config.keys():
                raise exceptions.ValidationError

    def update_config(self, **kwargs):
        config = update(self.config, kwargs)
        self.check_config(config)
        return config
