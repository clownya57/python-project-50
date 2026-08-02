from gendiff.diff_builder import (
    ADDED,
    CHANGED,
    NESTED,
    REMOVED,
)


def stringify(value):
    if isinstance(value, (dict, list)):
        return '[complex value]'

    if isinstance(value, str):
        return f"'{value}'"

    if isinstance(value, bool):
        return str(value).lower()

    if value is None:
        return 'null'

    return str(value)


def build_property_path(parent_path, key):
    if parent_path:
        return f'{parent_path}.{key}'

    return key


def format_added(path, value):
    formatted_value = stringify(value)

    return (
        f"Property '{path}' was added with value: "
        f'{formatted_value}'
    )


def format_removed(path):
    return f"Property '{path}' was removed"


def format_changed(path, old_value, new_value):
    formatted_old_value = stringify(old_value)
    formatted_new_value = stringify(new_value)

    return (
        f"Property '{path}' was updated. "
        f'From {formatted_old_value} '
        f'to {formatted_new_value}'
    )


def walk(diff, parent_path):
    lines = []

    for node in diff:
        node_type = node['type']
        path = build_property_path(
            parent_path,
            node['key'],
        )

        if node_type == NESTED:
            lines.extend(
                walk(node['children'], path)
            )

        elif node_type == ADDED:
            lines.append(
                format_added(path, node['value'])
            )

        elif node_type == REMOVED:
            lines.append(
                format_removed(path)
            )

        elif node_type == CHANGED:
            lines.append(
                format_changed(
                    path,
                    node['old_value'],
                    node['new_value'],
                )
            )

    return lines


def format_plain(diff):
    return '\n'.join(walk(diff, ''))
