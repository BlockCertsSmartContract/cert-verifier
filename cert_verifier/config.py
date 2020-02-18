import os
import configargparse
from web3 import Web3, HTTPProvider

_cwd = "WILL BE SET IN INIT"
_CONFIG = None


def add_arguments(p):
    p.add('-c', '--my-config', required=False, env_var='CONFIG_FILE',
          is_config_file=True, help='config file path')
    p.add_argument('--node_ropsten', help='infura ropsten', env_var='INFURA_ROPSTEN')
    p.add_argument('--node_mainnet', help='infura mainnet', env_var='INFURA_MAINNET')
    p.add_argument('--ens_registry', required=False, default="0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
                   help='mainnet', env_var='REGISTRY')


def read_config():
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(_cwd, 'config.ini')])
    add_arguments(p)
    parsed_config, _ = p.parse_known_args()
    return vars(parsed_config)


def init_config():
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = read_config()
    else:
        return _CONFIG


def get_infura(chain):
    init_config()
    global _CONFIG
    if chain == "ethereumMainnet":
        return _CONFIG["node_mainnet"]
    else:
        return _CONFIG["node_ropsten"]


def get_registry():
    init_config()
    global _CONFIG
    w3 = Web3(HTTPProvider())
    return w3.toChecksumAddress(_CONFIG["ens_registry"])
