import pathlib

import invoke
from setuptools_scm import version_from_scm

from .utils import check_tools


@invoke.task
@check_tools('devpi', 'true')
def release(ctx):
    if not version_from_scm('.').exact:
        raise RuntimeError('dirty versions is not for release')
    ctx.run('python setup.py bdist_wheel')
    packages = list(pathlib.Path('dist').glob('*'))
    if len(packages) != 1:
        raise RuntimeError('please cleanup (especially dist) before release')
    ctx.run(f'devpi upload {packages[0]}')
