ADDED = 'added'
REMOVED = 'removed'
UNCHANGED = 'unchanged'
CHANGED = 'changed'
NESTED = 'nested'


def build_diff(data1, data2):
    nodes = []

    for key in sorted(set(data1) | set(data2)):
        if key not in data1:
            nodes.append({
                'key': key,
                'type': ADDED,
                'value': data2[key],
            })

        elif key not in data2:
            nodes.append({
                'key': key,
                'type': REMOVED,
                'value': data1[key],
            })

        elif (
            isinstance(data1[key], dict)
            and isinstance(data2[key], dict)
        ):
            nodes.append({
                'key': key,
                'type': NESTED,
                'children': build_diff(
                    data1[key],
                    data2[key],
                ),
            })

        elif data1[key] == data2[key]:
            nodes.append({
                'key': key,
                'type': UNCHANGED,
                'value': data1[key],
            })

        else:
            nodes.append({
                'key': key,
                'type': CHANGED,
                'old_value': data1[key],
                'new_value': data2[key],
            })

    return tuple(nodes)
