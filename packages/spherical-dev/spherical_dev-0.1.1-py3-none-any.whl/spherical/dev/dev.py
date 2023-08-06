import invoke


@invoke.task
def dev(ctx):
    ctx.run('pip install -e .[dev]')
