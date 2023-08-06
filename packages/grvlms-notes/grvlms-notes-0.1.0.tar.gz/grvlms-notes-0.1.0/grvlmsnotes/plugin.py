import click
from glob import glob
import os

from .__about__ import __version__
from grvlms.commands import config as config_cli
from grvlms import config as grvlms_config
from grvlms import env
from grvlms import interactive

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 24|random_string }}",
        "OAUTH2_KEY": "{{ 8|random_string }}"
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "groovetech/openedx-notes:{{ NOTES_VERSION }}",
        "HOST": "notes.{{ WILDCARD_DOMAIN }}",
        "MYSQL_DATABASE": "notes",
        "MYSQL_USERNAME": "notes",
    },
}

hooks = {
    "init": ["mysql", "lms", "notes"],
    "build-image": {"notes": "{{ NOTES_DOCKER_IMAGE }}"},
    "remote-image": {"notes": "{{ NOTES_DOCKER_IMAGE }}"},
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches

@click.group(help="Extra Command for Notes")
def command():
    pass

@click.command(help="Print Notes version", name="version")
def print_version():
    click.secho("The version is: {}".format(__version__), fg="blue")

def ask_questions_notes(config, defaults):
    interactive.ask(
        "MYSQL Passwork:",
        "NOTES_MYSQL_PASSWORD",
        config,
        {"NOTES_MYSQL_PASSWORD": ""}
    )
    interactive.ask(
        "Secret Key:",
        "NOTES_SECRET_KEY",
        config,
        {"NOTES_SECRET_KEY": ""}
    )
    interactive.ask(
        "Oauth2 Secret:",
        "NOTES_OAUTH2_SECRET",
        config,
        {"NOTES_OAUTH2_SECRET": ""}
    )
    interactive.ask(
        "Oauth2 Key:",
        "NOTES_OAUTH2_KEY",
        config,
        {"NOTES_OAUTH2_KEY": ""}
    )
    interactive.ask(
        "MYSQL Database:",
        "NOTES_MYSQL_DATABASE",
        config,
        {"NOTES_MYSQL_DATABASE": ""}
    )
    interactive.ask(
        "MYSQL Username:",
        "NOTES_MYSQL_USERNAME",
        config,
        {"NOTES_MYSQL_USERNAME": ""}
    )

def load_config_notes(root, interactive=True):
    defaults = grvlms_config.load_defaults()
    config = grvlms_config.load_current(root, defaults)
    if interactive:
        ask_questions_notes(config, defaults)
    return config, defaults

@click.command(help="Notes variables configuration", name="config")
@click.option("-i", "--interactive", is_flag=True, help="Run interactively")
@click.option("-s", "--set", "set_",
    type=config_cli.YamlParamType(),
    multiple=True,
    metavar="KEY=VAL", 
    help="Set a configuration value")
@click.pass_obj
def config_notes(context, interactive, set_):
    config, defaults = load_config_notes(
        context.root, interactive=interactive
    )
    if set_:
        grvlms_config.merge(config, dict(set_), force=True)
    grvlms_config.save_config_file(context.root, config)
    grvlms_config.merge(config, defaults)
    env.save(context.root, config)

command.add_command(print_version)
command.add_command(config_notes)
