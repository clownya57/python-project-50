from gendiff.diff_builder import (
    ADDED,
    CHANGED,
    NESTED,
    REMOVED,
    UNCHANGED,
)

SPACES_COUNT = 4
LEFT_SHIFT = 2


def normalize(value):
    if isinstance(value, bool):
        return str(value).lower()

    if value is None:
        return 'null'

    return str(value)


def stringify(value, depth):
    if not isinstance(value, dict):
        return normalize(value)

    lines = ['{']
    indent = ' ' * ((depth + 1) * SPACES_COUNT)
    closing_indent = ' ' * (depth * SPACES_COUNT)

    for key in sorted(value):
        nested_value = stringify(
            value[key],
            depth + 1,
        )
        lines.append(
            f'{indent}{key}: {nested_value}'
        )

    lines.append(f'{closing_indent}}}')

    return '\n'.join(lines)


def format_stylish(diff, depth=1):
    lines = ['{']

    sign_indent = ' ' * (
        depth * SPACES_COUNT - LEFT_SHIFT
    )
    plain_indent = ' ' * (
        depth * SPACES_COUNT
    )

    for node in diff:
        key = node['key']
        node_type = node['type']

        if node_type == NESTED:
            children = format_stylish(
                node['children'],
                depth + 1,
            )
            lines.append(
                f'{plain_indent}{key}: {children}'
            )

        elif node_type == ADDED:
            value = stringify(
                node['value'],
                depth,
            )
            lines.append(
                f'{sign_indent}+ {key}: {value}'
            )

        elif node_type == REMOVED:
            value = stringify(
                node['value'],
                depth,
            )
            lines.append(
                f'{sign_indent}- {key}: {value}'
            )

        elif node_type == UNCHANGED:
            value = stringify(
                node['value'],
                depth,
            )
            lines.append(
                f'{plain_indent}{key}: {value}'
            )

        elif node_type == CHANGED:
            old_value = stringify(
                node['old_value'],
                depth,
            )
            new_value = stringify(
                node['new_value'],
                depth,
            )

            lines.append(
                f'{sign_indent}- {key}: {old_value}'
            )
            lines.append(
                f'{sign_indent}+ {key}: {new_value}'
            )

    closing_indent = ' ' * (
        (depth - 1) * SPACES_COUNT
    )
    lines.append(f'{closing_indent}}}')

    return '\n'.join(lines)
