import json
import sys
from pathlib import Path

import pytest

from gendiff import generate_diff
from gendiff.scripts.gendiff import main

TEST_DATA_DIR = Path(__file__).parent / 'test_data'

INPUT_CASES = [
    (
        'nested_file1.json',
        'nested_file2.json',
    ),
    (
        'nested_file1.yml',
        'nested_file2.yaml',
    ),
]

FORMAT_CASES = [
    (
        'stylish',
        'expected_nested_stylish.txt',
    ),
    (
        'plain',
        'expected_plain.txt',
    ),
    (
        'json',
        'expected_json.json',
    ),
]


def get_test_data_path(filename):
    return TEST_DATA_DIR / filename


def read_test_data(filename):
    filepath = get_test_data_path(filename)
    return filepath.read_text(
        encoding='utf-8',
    ).rstrip('\n')


def assert_result(actual, expected, format_name):
    if format_name == 'json':
        assert json.loads(actual) == json.loads(expected)
    else:
        assert actual == expected


@pytest.mark.parametrize(
    ('file1_name', 'file2_name'),
    INPUT_CASES,
)
@pytest.mark.parametrize(
    ('format_name', 'expected_name'),
    FORMAT_CASES,
)
def test_generate_diff(
    file1_name,
    file2_name,
    format_name,
    expected_name,
):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
    expected = read_test_data(expected_name)

    actual = generate_diff(
        file1,
        file2,
        format_name,
    )

    assert_result(actual, expected, format_name)


@pytest.mark.parametrize(
    ('file1_name', 'file2_name'),
    INPUT_CASES,
)
def test_default_format(file1_name, file2_name):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
    expected = read_test_data(
        'expected_nested_stylish.txt',
    )

    actual = generate_diff(file1, file2)

    assert actual == expected


@pytest.mark.parametrize(
    ('format_name', 'expected_name'),
    FORMAT_CASES,
)
def test_cli(
    monkeypatch,
    capsys,
    format_name,
    expected_name,
):
    file1 = get_test_data_path(
        'nested_file1.json',
    )
    file2 = get_test_data_path(
        'nested_file2.json',
    )
    expected = read_test_data(expected_name)

    monkeypatch.setattr(
        sys,
        'argv',
        [
            'gendiff',
            '--format',
            format_name,
            str(file1),
            str(file2),
        ],
    )

    main()

    actual = capsys.readouterr().out.rstrip('\n')

    assert_result(actual, expected, format_name)
