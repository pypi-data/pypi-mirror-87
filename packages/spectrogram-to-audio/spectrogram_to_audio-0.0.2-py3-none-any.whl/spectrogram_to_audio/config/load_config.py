import os
from dynaconf import Dynaconf


def load_config():
    relative_abs_path = os.path.dirname(__file__)
    conf_file = "config-default.yaml"
    abs_path = os.path.join(relative_abs_path, os.path.join("config_files", conf_file))
    return Dynaconf(
        ENVVAR_PREFIX_FOR_DYNACONF=False,
        core_loaders='YAML',
        settings_files=[abs_path]
    )


config = load_config()
