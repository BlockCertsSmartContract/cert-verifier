import os
import configargparse
from web3 import Web3, HTTPProvider

cwd = os.path.dirname(os.path.abspath(__file__))
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
    add_arguments(p)
    parsed_config, _ = p.parse_known_args()
    return vars(parsed_config)


def init_config():
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = read_config()
    else:
        return _CONFIG


def get_chain():
    init_config()
    global _CONFIG
    return _CONFIG["chain"]


def get_infura():
    init_config()
    global _CONFIG
    if get_chain() == "mainnet":
        return _CONFIG["infura_mainnet"]
    else:
        return _CONFIG["infura_ropsten"]


def get_registry():
    init_config()
    global _CONFIG
    w3 = Web3(HTTPProvider())
    if get_chain() == "mainnet":
        return w3.toChecksumAddress(_CONFIG["ethereum_mainnet"])
    else:
        return w3.toChecksumAddress(_CONFIG["ethereum_ropsten"])
