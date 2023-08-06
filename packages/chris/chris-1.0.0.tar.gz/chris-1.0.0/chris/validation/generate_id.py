"""Generator or unique IDs."""
import argparse
import uuid


def parse_args():
    """Parse script args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default=1, type=int)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    for _ in range(args.n):
        print(str(uuid.uuid4()))
