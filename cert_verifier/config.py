import os
import configargparse

cwd = os.getcwd()
_CONFIG = None


def add_arguments(p):
    p.add('-c', '--my-config', required=False, env_var='CONFIG_FILE',
          is_config_file=True, help='config file path')
    p.add_argument('--infura_ropsten', help='infura ropsten', env_var='INFURA_ROPSTEN')
    p.add_argument('--infura_mainnet', help='infura mainnet', env_var='INFURA_MAINNET')
    p.add_argument('--ethereum_mainnet', help='registry mainnet', env_var='REGISTRY_ROPSTEN')
    p.add_argument('--ethereum_ropsten', help='registry ropsten', env_var='REGISTRY_MAINNET')
    p.add_argument('--chain', help='chain', env_var='CHAIN')


def read_config():
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(cwd, 'config.ini')])
    print(cwd)
    add_arguments(p)
    parsed_config, _ = p.parse_known_args()
    return vars(parsed_config)


def init_config():
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = read_config()
    else:
        return _CONFIG


def get_infura():
    init_config()
    global _CONFIG
    if _CONFIG["chain"] == "ropsten":
        return _CONFIG["infura_ropsten"]
    elif _CONFIG["chain"] == "mainnet":
        return _CONFIG["infura_mainnet"]
    else:
        return False


def get_registry():
    init_config()
    global _CONFIG
    if _CONFIG["chain"] == "ropsten":
        return _CONFIG["ethereum_ropsten"]
    elif _CONFIG["chain"] == "mainnet":
        return _CONFIG["ethereum_mainnet"]
    else:
        return False
