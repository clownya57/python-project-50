import sys
from pathlib import Path

from gendiff import generate_diff
from gendiff.scripts.gendiff import main

TEST_DATA_DIR = Path(__file__).parent / 'test_data'


def get_test_data_path(filename):
    return TEST_DATA_DIR / filename


def read_test_data(filename):
    filepath = get_test_data_path(filename)
    return filepath.read_text(encoding='utf-8').rstrip()


def test_generate_diff():
    file1 = get_test_data_path('file1.json')
    file2 = get_test_data_path('file2.json')
    expected = read_test_data('expected_stylish.txt')

    actual = generate_diff(file1, file2)

    assert actual == expected


def test_cli(monkeypatch, capsys):
    file1 = get_test_data_path('file1.json')
    file2 = get_test_data_path('file2.json')
    expected = read_test_data('expected_stylish.txt')

    monkeypatch.setattr(
        sys,
        'argv',
        ['gendiff', str(file1), str(file2)],
    )

    main()

    captured = capsys.readouterr()

    assert captured.out == f'{expected}\n'
