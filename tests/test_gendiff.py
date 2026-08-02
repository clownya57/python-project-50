import sys
from pathlib import Path

import pytest

from gendiff import generate_diff
from gendiff.scripts.gendiff import main

TEST_DATA_DIR = Path(__file__).parent / 'test_data'

TEST_CASES = [
    ('file1.json', 'file2.json'),
    ('file1.yml', 'file2.yaml'),
]


def get_test_data_path(filename):
    return TEST_DATA_DIR / filename


def read_test_data(filename):
    filepath = get_test_data_path(filename)
    return filepath.read_text(encoding='utf-8').rstrip('\n')


@pytest.mark.parametrize(
    ('file1_name', 'file2_name'),
    TEST_CASES,
)
def test_generate_diff(file1_name, file2_name):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
    expected = read_test_data('expected_stylish.txt')

    actual = generate_diff(file1, file2)

    assert actual == expected


@pytest.mark.parametrize(
    ('file1_name', 'file2_name'),
    TEST_CASES,
)
def test_cli(monkeypatch, capsys, file1_name, file2_name):
    file1 = get_test_data_path(file1_name)
    file2 = get_test_data_path(file2_name)
    expected = read_test_data('expected_stylish.txt')

    monkeypatch.setattr(
        sys,
        'argv',
        ['gendiff', str(file1), str(file2)],
    )

    main()

    captured = capsys.readouterr()

    assert captured.out == f'{expected}\n'
