import invoke


@invoke.task
def isort(ctx, check_only=False):
    ctx.run(
        'isort -y -m 3 -lai 2 -tc '
        f'{"-c " if check_only else ""}'
        '-sg "alembic/*"'
    )
