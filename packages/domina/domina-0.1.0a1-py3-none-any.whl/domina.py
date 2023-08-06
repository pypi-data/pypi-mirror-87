import domina_util as util

import click

VERSION='0.1'

PATH_SRC='src'
PATH_BUILD='build'
PATH_DIST='dist'

URL_UPSTREAM = util.getenv(
    'DOMINA_URL_UPSTREAM',
    default='https://gitlab.com/screeps-domina/domina')

PATH_CONFIG_SAMPLE = util.getenv(
    'DOMINA_PATH_CONFIG_SAMPLE',
    default='config.sample.json')
PATH_CONFIG = util.getenv(
    'DOMINA_PATH_CONFIG',
    default='config.json')

GEN = util.getenv(
    'DOMINA_GEN',
    default=util.get_latest_generation(PATH_CONFIG)['gen'])
GENERATION = util.get_generation(PATH_CONFIG, GEN)

DEPLOY_TARGET = util.getenv(
    'DOMINA_DEPLOY_TARGET',
    default='screeps.com')

BUILD_PATHS = dict(
    path_src= util.join(PATH_SRC, GENERATION['name']),
    path_build = util.join(PATH_BUILD, GENERATION['name']),
    path_dist = util.join(PATH_DIST, GENERATION['name']),
)

@click.group()
def cli():
    '''Evolving game AI script framework for MMORTS screeps.com. Can be
    used to play screeps from a remote machine, or build CI/CD
    pipelines with comfort.

    It is presumed you want to manage your latest generation. You can
    override this behavior by setting the DOMINA_GEN environment
    variable to a desired number.

    '''
    pass

@cli.command('version')
@click.option('--local', '-l', is_flag=True,
              help='Print the version of current directory.')
def cmd_version(local):
    '''Print the version.'''
    click.echo(VERSION if not local else util.read_version())

@cli.command('init')
def cmd_init():
    '''Initialize domina in current directory.'''
    branch='feature/domina-cli'
    util.download_file(f'{URL_UPSTREAM}/-/raw/{branch}/{PATH_CONFIG_SAMPLE}',
                       PATH_CONFIG_SAMPLE)

@cli.group('list')
def list_():
    '''List available objects.'''
    pass

@list_.command('generations')
def cmd_list_generations():
    '''List generations specified in configuration.'''
    for generation in util.get_generations(PATH_CONFIG):
        click.echo(f'[{generation["gen"]}] {generation["name"]}')

@list_.command('targets')
def cmd_list_targets():
    '''List targets specified in configuration.'''
    for target in util.get_names(util.get_targets(PATH_CONFIG)):
        click.echo(target)

@cli.command('configure')
@click.option('--init', '-I', is_flag=True,
              help='Always initialize with latest configuration.')
@click.option('--pass', '-p' 'pass_name',
              metavar='<pass-name>', default=False,
              help='Use pass variable as sample config.')
@click.option('--overwrite', '-f', is_flag=True,
              help='Overwrite existing configuration.')
@click.option('--edit/--no-edit', default=False,
              help='Edit configuration file.')
@click.option('--download/--skip-download' '-d', default=False,
              help='Download source files.')
def cmd_configure(pass_name, overwrite, edit, download):
    '''Configure this repository.'''
    if not util.file_exists(PATH_CONFIG) or overwrite:
        if pass_name:
            util.pass_to_file(PATH_CONFIG, pass_name)
        elif util.file_exists(PATH_CONFIG_SAMPLE):
            util.copy(PATH_CONFIG_SAMPLE, PATH_CONFIG)
    if edit:
        util.open_editor(PATH_CONFIG)
    if download:
        util.clone_sources(PATH_CONFIG, PATH_SRC)

@cli.command('compile')
@click.option('--flatten/--no-flatten', default=True,
              help='Flatten nested submodules', show_default=True)
def cmd_compile(flatten):
    '''Build the project.'''
    util.build_project(flatten, **BUILD_PATHS)

@cli.command('test')
@click.option('--build/--no-build', default=True,
              help='Compile source files', show_default=True)
def cmd_test(build):
    '''Test the built project.'''
    if build:
        util.build_project(distribute=False, **BUILD_PATHS)
    util.test_project(util.join(PATH_BUILD, GENERATION['name']))

@cli.command('deliver')
@click.argument('target')
@click.confirmation_option(prompt='Are you sure?')
@click.option('--dry-run', '-C', is_flag=True, default=False,
              help='Do not affect the target')
@click.option('--build/--no-build', default=True,
              help='Compile source files', show_default=True)
@click.option('--test/--skip-test', default=True,
              help='Run tests (implicit --build)', show_default=True)
def cmd_deliver(target, build, test, dry_run):
    '''Deliver the project to TARGET.'''
    target = util.get_target(PATH_CONFIG, target)
    if target is None:
        raise click.BadParameter(
            util.get_names(util.get_targets(PATH_CONFIG)),
            param=target, param_hint='TARGET: Acceptable values are')
    util.deliver_project(target, build, test, dry_run, **BUILD_PATHS)

@cli.command('deploy')
@click.confirmation_option(prompt='Are you sure?')
@click.option('--dry-run', '-C', is_flag=True, default=False,
              help='Do not affect the target')
@click.option('--build/--no-build', default=True,
              help='Compile source files', show_default=True)
@click.option('--test/--skip-test', default=True,
              help='Run tests (implicit --build)', show_default=True)
def cmd_deploy(build, test, dry_run):
    '''Deploy the project to official server.'''
    target = util.get_target(PATH_CONFIG, 'screeps.com')
    util.deliver_project(target, build, test, dry_run, **BUILD_PATHS)

@click.command('distribute')
@click.confirmation_option(prompt=f'Distribute domina-{util.read_version()}?')
@click.option('--dry-run', '-C', is_flag=True, default=False,
              help='Do not affect the target')
@click.option('--pass', '-p', 'pass_name',
              metavar='<pass-name>', default=False,
              help='Use pass variable as release token.')
def cmd_distribute(pass_name, dry_run):
    '''(dev) Build and distribute domina itself.'''
    token = util.pass_decrypt(pass_name) \
        if pass_name else None
    util.distribute_domina(PATH_DIST, token=token)

if __name__ == '__main__':
    cli.add_command(cmd_distribute)
    cli()
