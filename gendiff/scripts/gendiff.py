import argparse
import json

DESCRIPTION = 'Compares two configuration files and shows a difference.'

def parse_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description=DESCRIPTION,
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        metavar='FORMAT',
        default='stylish',
        help='set format of output',
    )
    return parser.parse_args()

def parse_file(filepath):
    with open(filepath, encoding='utf-8') as file:
        return json.load(file)

def main():
    args = parse_args()
    parse_file(args.first_file)
    parse_file(args.second_file)

if __name__ == '__main__':
    main()
