from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish

FORMATTERS = {
    'plain': format_plain,
    'stylish': format_stylish,
}


def format_diff(diff, format_name):
    formatter = FORMATTERS.get(format_name)

    if formatter is None:
        raise ValueError(
            f'Unknown format: {format_name}'
        )

    return formatter(diff)
