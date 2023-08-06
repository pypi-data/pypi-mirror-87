import argparse
import os


def setup_argument_parser():
    ap = argparse.ArgumentParser(
        description="ScalaCCF - utility to fix style and documentation comments in Scala files")
    ap.add_argument('-p', type=str, default=None, help="Path to scala project directory to fix.")
    ap.add_argument('-d', type=str, default=None, help="Path to directory with Scala files to fix.")
    ap.add_argument('-f', type=str, default=None, help="Path to Scala file to fix.")
    ap.add_argument('-v', '--verify', action='store_true', help='Verify style and documentation comments')
    ap.add_argument('-t', '--trace', action='store_true', help='Fix style and documentation comments')
    return ap


def get_argument(possible_args, args):
    count = 0
    arg = None

    for i in possible_args:
        if getattr(args, i) not in (None, False):
            count += 1
            arg = i

    if arg is None or count != 1:
        raise ValueError(f'One of parameters {possible_args} must be present')
    return arg


def get_files(args, path_arg):
    result = None
    if path_arg == 'p':
        result = [os.path.join(path, f)
                  for path, dirs, fs in os.walk(args.p)
                  for f in fs
                  if os.path.isfile(os.path.join(path, f)) and (f.endswith('.scl') or f.endswith('.scala'))]
    if path_arg == 'd':
        result = [os.path.join(args.d, f)
                  for f in os.listdir(args.d)
                  if os.path.isfile(os.path.join(args.d, f)) and (f.endswith('.scl') or f.endswith('.scala'))]
    if path_arg == 'f':
        result = [args.f if args.f.endswith('.scl') or args.f.endswith('.scala') else None]

    return result
