import json
from pathlib import Path

import yaml

PARSERS = {
    '.json': json.load,
    '.yml': yaml.safe_load,
    '.yaml': yaml.safe_load,
}


def parse(filepath):
    path = Path(filepath)
    parser = PARSERS.get(path.suffix.lower())

    if parser is None:
        raise ValueError(
            f'Unsupported file format: {path.suffix}'
        )

    with path.open(encoding='utf-8') as file:
        return parser(file)
