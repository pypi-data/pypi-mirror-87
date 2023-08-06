import invoke


@invoke.task
def flake(ctx):
    ctx.run('flake8 --max-line-length=127')
