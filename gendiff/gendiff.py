from gendiff.parser import parse


def _stringify(value):
    if isinstance(value, bool):
        return str(value).lower()

    if value is None:
        return 'null'

    return str(value)


def _build_lines(key, data1, data2):
    if key not in data2:
        return (
            f'  - {key}: {_stringify(data1[key])}',
        )

    if key not in data1:
        return (
            f'  + {key}: {_stringify(data2[key])}',
        )

    if data1[key] == data2[key]:
        return (
            f'    {key}: {_stringify(data1[key])}',
        )

    return (
        f'  - {key}: {_stringify(data1[key])}',
        f'  + {key}: {_stringify(data2[key])}',
    )


def generate_diff(file_path1, file_path2):
    data1 = parse(file_path1)
    data2 = parse(file_path2)

    keys = sorted(set(data1) | set(data2))

    body = [
        line
        for key in keys
        for line in _build_lines(key, data1, data2)
    ]

    return '\n'.join(['{', *body, '}'])
