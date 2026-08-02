from gendiff.diff_builder import build_diff
from gendiff.formatters import format_diff
from gendiff.parser import parse


def generate_diff(
    file_path1,
    file_path2,
    format_name='stylish',
):
    data1 = parse(file_path1)
    data2 = parse(file_path2)

    diff = build_diff(data1, data2)

    return format_diff(diff, format_name)
