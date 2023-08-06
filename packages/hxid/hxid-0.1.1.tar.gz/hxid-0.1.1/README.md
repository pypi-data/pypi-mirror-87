# Homex HXID Generator Library for Python
This is a Python implementation of HXID (HomeX ID) generation and validation. It is intended to be used by both systems that generate HXIDs and systems that want to validate existing HXIDs.

## Requirements
This project requires Python version >=3.6.

## Installation
Add `hxid>=0.1.0` to your `requirements.txt` file or simply install locally with:
```
pip install hxid
```

## Usage
The available public methods include:

 - `def generate_hxid(prefix: str, seed:str, config: HxidConfig = None, appendage_configs: List[HxidConfig] = []) -> str`
 - `def is_hxid(candidate: str) -> bool`

Also, there is a public class constructor for generating HXID config objects:

 - `HxidConfig(prefix: str, seed: str, target_length: int = 9, collision_incrementor: int = 0)`

For optimal use of this package, generate your `HxidConfig` objects and pass these into `generate_hxid` to produce your HXIDs.

## Testing & Contributing
Run tests locally with
```
python -m unittest tests/test_hxid.py
```
The test suite will be checked for any Pull Requests made to this repository.  Please adapt the tests to your proposed changes for contributing.