import os
import shlex
import sys
import termios
import tty


def ask(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    sys.stdout.write(os.linesep)
    return ch


def flatten_options(labels, prefix=''):
    """Converts hierarchical list of dot separated options to dict of flat one.

    This structure:
    {'aaa':'b(`f`)','ccc.rrr':{'ddd':'eee',}}
    with prefix 'traefik' will be converted to:
    {'traefik.aaa': 'b(`f`)', 'traefik.ccc.rrr.ddd': 'eee'}
    """
    def flatten(labels, prefix):
        for name, value in labels.items():
            if prefix:
                name = f'{prefix}.{name}'
            if isinstance(value, dict):
                yield from flatten(value, name)
            else:
                yield name, value
    return dict(flatten(labels, prefix))


def named_args(flag, dct):
    """This function converts dict of named args to string of options for
    use in command line (f.e. env or label docker params).

    This structure:
    {'traefik.aaa': 'b(`f`)', 'traefik.ccc.rrr.ddd': 'eee'}
    will be converted to:
    "--label traefik.aaa='b(`f`)' --label traefik.ccc.rrr.ddd=eee"
    """
    return ' '.join(f'{flag}{k}={shlex.quote(str(v))}' for k, v in dct.items())
