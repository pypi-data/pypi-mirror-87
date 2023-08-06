import click
import os
import json
import shutil

from os import getcwd as rootdir
from os import getenv
from os.path import join
from os.path import isfile as file_exists
from os.path import isdir as directory_exists
from shutil import rmtree as remove
from subprocess import run

GEN_0 = dict(gen=0, name='0')

def get_names(dicts):
    return list(map(lambda t: t['name'], dicts))

def colorline(color, status, *msg):
    return click.echo(' '.join([click.style(status, fg=color), *msg]))

def stepline(*msg):
    return colorline('green', '*', *msg)

def clickfail(msg):
    click.get_current_context().fail(msg)

def check_file_exists(path):
    if not file_exists(path):
        raise click.FileError(path, hint='No such file')

def open_editor(path):
    stepline(f'Editing {path}')
    check_file_exists(path)
    click.edit(filename=path)

def pass_decrypt(pass_name):
    stepline(f'Decrypting <{pass_name}>')
    return str(run(f'pass show {pass_name}'.split(),
                   capture_output=True).stdout, encoding='utf-8')

def pass_to_file(path, pass_name):
    decrypted_pass = pass_decrypt(pass_name)
    with open(path, 'w') as f:
        f.writelines(decrypted_pass)

def download_file(url, path):
    stepline(f'Downloading {url} to {path}')
    run(f'curl {url} -o {path}'.split())

def read_file(path):
    check_file_exists(path)
    with open(path, 'r') as f:
        return f.read()

def read_json(path):
    return json.loads(read_file(path))

def read_about():
    return str(read_file('ABOUT'))

def read_version():
    return str(read_file('VERSION'))

def get_targets(path_config):
    return read_json(path_config)['targets']

def get_target(path_config, name, fail=False):
    targets, target = get_targets(path_config), None
    for t in filter(lambda t: t['name'] == name, targets):
        target = t
        break
    if fail and target is None:
        raise click.BadParameter(
            get_names(get_targets(path_config)),
            param=target,
            param_hint='TARGET: Acceptable values are'
        )
    return target

def get_generations(path_config):
    return read_json(path_config)['evolution']

def get_generation(path_config, gen, fail=False):
    for generation in get_generations(path_config):
        if generation['gen'] == gen:
            return generation
    if fail:
        clickfail(f'No generation with gen: {gen}')
    return GEN_0

def get_latest_generation(path_config):
    latest, gen = None, int()
    for generation in get_generations(path_config):
        if generation['gen'] >= gen:
            latest, gen = generation, generation['gen']
    return latest if latest is not None else GEN_0

def copy(path_orig, path_dest):
    if directory_exists(path_orig):
        stepline(f'Copying directory {path_orig} over {path_dest}')
        shutil.copytree(path_orig, path_dest)
    elif file_exists(path_orig):
        stepline(f'Copying file {path_orig} over {path_dest}')
        shutil.copy(path_orig, path_dest)
    else:
        raise click.FileError(path_orig, hint='No such file')

def clone_sources(path_config, path_src):
    if not directory_exists(path_src):
        os.makedirs(path_src)
    for gen in get_generations(path_config):
        if 'git' in gen:
            version = gen.setdefault('version', 'master')
            stepline(f'Cloning {gen["name"]} at {version}')
            run(['git', 'clone {gen["git"]}',
                 '{path_src}/{gen["name"]}',
                 '-b {version}'])

def flatten_submodules(path_root):
    pass

def run_tests(path):
    path_bin_mocha = './node_modules/mocha/bin/mocha'
    process = run(f'{path_bin_mocha} {path}', shell=True)
    return process.returncode == 0

def test_project(path_build, fail=False):
    stepline('Running test suites')
    test_ok = run_tests(join(path_build, 'test'))
    if not test_ok and fail:
        fail('Failed to pass the tests.')
    return test_ok

def build_project(flatten=True, test=False, distribute=True,
                  path_src=None, path_build='build', path_dist='dist'):
    if path_src is None or not directory_exists(path_src):
        msg = 'Source file not present'
        raise click.FileError(f'{path_src}/main/main.js', hint=msg)
    if directory_exists(path_build):
        stepline('Clearing previous build')
        remove(path_build)
    stepline('Copying source files')
    copy(path_src, path_build)
    stepline('Compiling source files')
    if flatten:
        stepline('Flattening source files')
        flatten_submodules(path_build)
    if test:
        test_project(path_build, fail=True)
    if distribute:
        if directory_exists(path_dist):
            stepline('Clearing previous artifacts')
            remove(path_dist)
        stepline('Copying artifacts')
        copy(path_build, path_dist)

def deliver_project(target, build, test, dry_run, **build_paths):
    if build or test:
        build_project(flatten=True, test=test, distribute=True,
                      **build_paths)
    if not dry_run:
        stepline(f'Delivering to {target["name"]}')

def distribute_domina(path_dist='dist', repo='pypi', token=None):
    version = read_version()
    artifacts = join(path_dist, 'domina-*')
    stepline('Clearing previous artifacts')
    run(f'rm -f {artifacts}'.split())
    stepline(f'Building domina-{version}')
    run('python setup.py sdist bdist_wheel'.split())
    if token is not None:
        stepline(f'Distributing domina-{version} to pypi')
        run(['twine', 'upload', artifacts, '-u', '__token__', '-p', token,
             '-r', repo], shell=True)

