import argparse

from gendiff import generate_diff

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

def main():
    args = parse_args()
    diff = generate_diff(
        args.first_file,
        args.second_file,
    )
    print(diff)

if __name__ == '__main__':
    main()
