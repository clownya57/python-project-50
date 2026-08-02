import sys
from pathlib import Path

import pytest

from gendiff import generate_diff
from gendiff.scripts.gendiff import main

TEST_DATA_DIR = Path(__file__).parent / 'test_data'

STYLISH_CASES = [
    (
        'file1.json',
        'file2.json',
        'expected_stylish.txt',
    ),
    (
        'file1.yml',
        'file2.yaml',
        'expected_stylish.txt',
    ),
    (
        'nested_file1.json',
        'nested_file2.json',
        'expected_nested_stylish.txt',
    ),
    (
        'nested_file1.yml',
        'nested_file2.yaml',
        'expected_nested_stylish.txt',
    ),
]

PLAIN_CASES = [
    (
        'nested_file1.json',
        'nested_file2.json',
    ),
    (
        'nested_file1.yml',
        'nested_file2.yaml',
    ),
]

CLI_CASES = [
    (
        'stylish',
        'nested_file1.json',
        'nested_file2.json',
        'expected_nested_stylish.txt',
    ),
    (
        'plain',
        'nested_file1.json',
        'nested_file2.json',
        'expected_plain.txt',
    ),
]


def get_test_data_path(filename):
    return TEST_DATA_DIR / filename


def read_test_data(filename):
    filepath = get_test_data_path(filename)
    return filepath.read_text(encoding='utf-8').rstrip('\n')


@pytest.mark.parametrize(
    ('file1_name', 'file2_name', 'expected_name'),
    STYLISH_CASES,
)
def test_generate_diff_stylish(
    file1_name,
    file2_name,
    expected_name,
):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
    expected = read_test_data(expected_name)

    assert generate_diff(file1, file2) == expected
    assert generate_diff(file1, file2, 'stylish') == expected


@pytest.mark.parametrize(
    ('file1_name', 'file2_name'),
    PLAIN_CASES,
)
def test_generate_diff_plain(
    file1_name,
    file2_name,
):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
    expected = read_test_data('expected_plain.txt')

    assert generate_diff(file1, file2, 'plain') == expected


@pytest.mark.parametrize(
    (
        'format_name',
        'file1_name',
        'file2_name',
        'expected_name',
    ),
    CLI_CASES,
)
def test_cli(
    monkeypatch,
    capsys,
    format_name,
    file1_name,
    file2_name,
    expected_name,
):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
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

    captured = capsys.readouterr()

    assert captured.out == f'{expected}\n'
