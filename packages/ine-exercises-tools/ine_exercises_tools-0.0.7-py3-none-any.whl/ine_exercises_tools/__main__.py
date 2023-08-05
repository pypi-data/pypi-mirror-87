import click
from ine_exercises_tools import strategies
from ine_exercises_tools.authenticator import Authenticator


def common_options(fn):
    fn = click.option('-g', '--gist_id', required=False)(fn)
    fn = click.option(
        '--development',
        is_flag=True,
        help="Will NOT use production APIs."
    )(fn)
    return fn


STRATEGIES = [
    strategies.GistStrategy
]

def resolve_strategy(*args, **kwargs):
    for Strategy in STRATEGIES:
        if Strategy.is_valid(*args, **kwargs):
            return Strategy()

    raise ValueError("Strategy not found!")


@click.group()
def cli():
    print()


@cli.command()
@common_options
def run(*args, **kwargs):
    strategy = resolve_strategy(*args, **kwargs)
    exercise = strategy.build_exercise(*args, **kwargs)
    exercise.run()


@cli.command()
@common_options
def test(*args, **kwargs):
    strategy = resolve_strategy(*args, **kwargs)
    exercise = strategy.build_exercise(*args, **kwargs)
    exercise.test()


@cli.command()
@common_options
@click.option('-u', '--username', required=True, prompt=True)
@click.password_option(confirmation_prompt=False)
@click.option('-c', '--client', required=True, prompt=True)
def create(*args, **kwargs):
    auth_token = Authenticator.get_token(
        username=kwargs['username'],
        password=kwargs['password'],
        client=kwargs['client'],
        development=kwargs.get('development', False),
    )
    strategy = resolve_strategy(*args, **kwargs)
    exercise = strategy.build_exercise(*args, **kwargs)
    exercise.create(auth_token=auth_token)


@cli.command()
@common_options
def update():
    click.echo('Syncing')


def main():
    cli()


if __name__ == "__main__":
    main()
