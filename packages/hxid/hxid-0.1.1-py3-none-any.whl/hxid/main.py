from hashlib import sha1
from typing import List

class HxidConfig:
    def __init__(self,
                 prefix: str,
                 seed: str,
                 target_length: int = 9,
                 collision_incrementor: int = 0):
        self.prefix = prefix
        self.seed = seed
        self.target_length = target_length
        self.collision_incrementor = collision_incrementor
        if target_length + collision_incrementor > 40:
            raise Exception("This id generator package does not support generating" + \
                            "hashes of greater than 40 characters. " + \
                            "Length of {target_length} + {collision_incrementor} " + \
                            "= {total_length} received.".format(
                                target_length = target_length,
                                collision_incrementor = collision_incrementor,
                                total_length = target_length + collision_incrementor
                            ))


def generate_hxid(prefix: str,
                  seed: str,
                  config: HxidConfig = None,
                  appendage_configs: List[HxidConfig] = []) -> str:

    _throw_if_bad_arguments(prefix, seed, config, appendage_configs)

    if not config:
        config = HxidConfig(prefix, seed)
    if not _is_hxid_config(config):
        raise Exception("Provided config must be valid.  Received: {config}"
                        .format(config=config))

    base = _generate_base_hxid(
        config.prefix,
        config.seed,
        config.target_length,
        config.collision_incrementor
    )
    appendages = map(_generate_appendage, appendage_configs)
    appendage_str = ""
    for appendage in appendages:
        appendage_str += appendage

    return base + appendage_str

def is_hxid(candidate: str) -> bool:
    prefix_suffix = candidate.split("-")
    if len(prefix_suffix) != 2 \
       or "HX" not in prefix_suffix[0] \
       or len(prefix_suffix[0]) > 5 \
       or len(prefix_suffix[0]) < 4:
        return False
    appendages_exist = [len(appendage) > 0 for appendage in prefix_suffix[1].split("_")]
    if not all(appendages_exist):
        return False
    return True

def _throw_if_bad_arguments(prefix: str,
                            seed: str,
                            config: HxidConfig,
                            appendage_configs: List[HxidConfig]) -> None:
    if not config:
        if type(prefix) is not str or len(prefix) < 2 or len(prefix) > 3:
            raise Exception("You must provide a string prefix of either " + \
                            "2 or 3 characters to this function in order " + \
                            "to generate an HXID. " +\
                            "Received: {prefix}".format(prefix = prefix))
        if type(seed) is not str or len(seed) < 1:
            raise Exception("You must provide a string seed to this " + \
                            "function in order to generate an HXID. " + \
                            "Received: {seed}".format(seed = seed))

    if config and not _is_hxid_config(config):
        raise Exception("The config argument must be a valid HXID config " + \
                        "object. You can generate one using the " + \
                        "generateHXIDConfig function. " + \
                        "Received: {config}".format(config = config))

    if appendage_configs is None or not all([isinstance(appendage, HxidConfig) for appendage in appendage_configs]):
        raise Exception("The appendage_configs argument must be an array of " + \
                        "valid HXID configs. You can generate one using " + \
                        "the generateHXIDConfig function. " + \
                        "Received: {appendage_configs}".format(
                            appendage_configs = appendage_configs
                        ))
    return None

def _is_hxid_config(config: HxidConfig) -> bool:
    return type(config) is HxidConfig

def _generate_base_hxid(prefix: str,
                        seed: str,
                        target_length: int = 9,
                        collision_incrementor: int = 0) -> str:
    return "HX" + prefix.upper() + "-" + _generate_hash(seed, target_length, collision_incrementor)

def _generate_appendage(config: HxidConfig) -> str:
    return "_" + _generate_hash(config.seed, config.target_length, config.collision_incrementor)

def _generate_hash(seed: str, target_length: int, collision_incrementor: int) -> str:
    hash = sha1(seed.encode()).hexdigest()
    total_length = target_length + collision_incrementor
    return hash[0:total_length]

