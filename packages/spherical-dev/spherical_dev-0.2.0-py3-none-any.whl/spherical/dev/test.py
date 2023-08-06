import os
import pathlib
import webbrowser

import invoke


@invoke.task
def test(
    ctx,
    coverage=False,
    deprecations=False,
    verbose=False,
    pdb=False,
    ipython=False,
    key=None,
    skip_capture=False,
):
    cwd = os.getcwd()
    ctx.run(
        ' '.join((
            'pytest',
            *(coverage and (f'--cov={cwd}', '--cov-report=html') or ()),
            *(verbose and ('-vv',) or ()),
            *(pdb and ('--pdb',) or ()),
            *(ipython and ('--pdbcls=spherical.dev.debugger:Debugger',) or ()),
            *(key and (f'-k {key}',) or ()),
            *(skip_capture and ('-s',) or ()),
        )),
        pty=True,
        env={} if deprecations else {
            'PYTHONWARNINGS': (
                'default,'
                'ignore::DeprecationWarning,'
                'ignore::ResourceWarning'
            ),
        },
    )
    report_index = pathlib.Path('htmlcov/index.html').resolve()
    if coverage:
        webbrowser.open(f'file:{report_index}')
