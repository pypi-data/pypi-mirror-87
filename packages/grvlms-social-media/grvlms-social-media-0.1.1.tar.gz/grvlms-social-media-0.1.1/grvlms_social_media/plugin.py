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
        # SOCIAL_SHARING_SETTINGS
        "SOCIAL_SHARING_SETTINGS": False,
        "CUSTOM_COURSE_URLS": False,
        "ACTIVATE_FACEBOOK": False,
        "DASHBOARD_FACEBOOK": False,
        "CERTIFICATE_FACEBOOK": False,
        "CERTIFICATE_FACEBOOK_TEXT": "",
        "FACEBOOK_BRAND": "",
        "ACTIVATE_TWITTER": False,
        "CERTIFICATE_TWITTER": False,
        "CERTIFICATE_TWITTER_TEXT": "",
        "DASHBOARD_TWITTER": False,
        "TWITTER_BRAND": "",
        "ENABLE_TWITTER_TEXT": False,
        "DASHBOARD_TWITTER_TEXT": "",
        "SOCIAL_MEDIA_FOOTER_NAMES": False,
        "SOCIAL_MEDIA_FOOTER_FACEBOOK": False,
        "SOCIAL_MEDIA_FOOTER_TWITTER": False,
        "SOCIAL_MEDIA_FOOTER_YOUTUBE": False,
        "SOCIAL_MEDIA_FOOTER_LINKEDIN": False,
        "SOCIAL_MEDIA_FOOTER_GOOGLE_PLUS": False,
        "SOCIAL_MEDIA_FOOTER_REDDIT": False,

        # SOCIAL_MEDIA_FOOTER_NAMES
        "SOCIAL_MEDIA_FOOTER_NAMES": False,
        "FOOTER_FACEBOOK": False,
        "FOOTER_TWITTER": False,
        "FOOTER_YOUTUBE": False,
        "FOOTER_LINKEDIN": False,
        "FOOTER_GOOGLE_PLUS": False,
        "FOOTER_REDDIT": False,
    }
}

hooks = {}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches

@click.group(help="Extra Command for Social Media Sharing")
def command():
    pass

@click.command(help="Print socialmedia version", name="version")
def print_version():
    click.secho("The version is: {}".format(__version__), fg="blue")

def ask_questions_socialmedia(config, defaults):
    # Enable Social Media Sharing
    interactive.ask_bool(
        "Enable Social Media Sharing:",
        "SOCIALMEDIA_SOCIAL_SHARING_SETTINGS",
        config,
        {"SOCIALMEDIA_SOCIAL_SHARING_SETTINGS": False}
    )
    if config["SOCIALMEDIA_SOCIAL_SHARING_SETTINGS"]:
        # Enable Custom Course Urls
        interactive.ask_bool(
            "Enable Custom Course Urls:",
            "SOCIALMEDIA_CUSTOM_COURSE_URLS",
            config,
            {"SOCIALMEDIA_CUSTOM_COURSE_URLS": False}
        )

        # Facebook
        interactive.ask_bool(
            "Activate Facebook:",
            "SOCIALMEDIA_ACTIVATE_FACEBOOK",
            config,
            {"SOCIALMEDIA_ACTIVATE_FACEBOOK": False}
        )
        if config["SOCIALMEDIA_ACTIVATE_FACEBOOK"]:
            interactive.ask_bool(
                "Enable Dashboard Facebook:",
                "SOCIALMEDIA_DASHBOARD_FACEBOOK",
                config,
                {"SOCIALMEDIA_DASHBOARD_FACEBOOK": False}
            )
            if config["SOCIALMEDIA_DASHBOARD_FACEBOOK"]:
                interactive.ask(
                    "Facebook Brand:",
                    "SOCIALMEDIA_FACEBOOK_BRAND",
                    config,
                    {"SOCIALMEDIA_FACEBOOK_BRAND": ""}
                )
            interactive.ask_bool(
                "Enable Certificate Facebook:",
                "SOCIALMEDIA_CERTIFICATE_FACEBOOK",
                config,
                {"SOCIALMEDIA_CERTIFICATE_FACEBOOK": False}
            )
            if config["SOCIALMEDIA_CERTIFICATE_FACEBOOK"]:
                interactive.ask(
                    "Certificate Facebook Text:",
                    "SOCIALMEDIA_CERTIFICATE_FACEBOOK_TEXT",
                    config,
                    {"SOCIALMEDIA_CERTIFICATE_FACEBOOK_TEXT": ""}
                )

        # Twitter
        interactive.ask_bool(
            "Activate Twitter:",
            "SOCIALMEDIA_ACTIVATE_TWITTER",
            config,
            {"SOCIALMEDIA_ACTIVATE_TWITTER": False}
        )
        if config["SOCIALMEDIA_ACTIVATE_TWITTER"]:
            interactive.ask_bool(
                "Enable Certificate Twitter:",
                "SOCIALMEDIA_CERTIFICATE_TWITTER",
                config,
                {"SOCIALMEDIA_CERTIFICATE_TWITTER": False}
            )
            if config["SOCIALMEDIA_CERTIFICATE_TWITTER"]:
                interactive.ask(
                    "Certificate Twitter Text:",
                    "SOCIALMEDIA_CERTIFICATE_TWITTER_TEXT",
                    config,
                    {"SOCIALMEDIA_CERTIFICATE_TWITTER_TEXT": False}
                )
            interactive.ask_bool(
                "Enable Dashboard Twitter:",
                "SOCIALMEDIA_DASHBOARD_TWITTER",
                config,
                {"SOCIALMEDIA_DASHBOARD_TWITTER": False}
            )
            if config["SOCIALMEDIA_DASHBOARD_TWITTER"]:
                interactive.ask(
                    "Twitter Brand:",
                    "SOCIALMEDIA_TWITTER_BRAND",
                    config,
                    {"SOCIALMEDIA_TWITTER_BRAND": ""}
                )
                interactive.ask_bool(
                    "Enable Twitter Text:",
                    "SOCIALMEDIA_ENABLE_TWITTER_TEXT",
                    config,
                    {"SOCIALMEDIA_ENABLE_TWITTER_TEXT": False}
                )
                if config["SOCIALMEDIA_ENABLE_TWITTER_TEXT"]:
                    interactive.ask(
                        "Dashboard Twitter Text:",
                        "SOCIALMEDIA_DASHBOARD_TWITTER_TEXT",
                        config,
                        {"SOCIALMEDIA_DASHBOARD_TWITTER_TEXT": False}
                    )
    interactive.ask_bool(
        "Enable Media Footer Names:",
        "SOCIALMEDIA_SOCIAL_MEDIA_FOOTER_NAMES",
        config,
        {"SOCIALMEDIA_SOCIAL_MEDIA_FOOTER_NAMES": False}
    )
    if config["SOCIALMEDIA_SOCIAL_MEDIA_FOOTER_NAMES"]:
        for social_name in ["facebook", "twitter", "youtube", "linkedin", "google_plus", "reddit"]:
            interactive.ask_bool(
                "Enable {name}:".format(name=social_name),
                "SOCIALMEDIA_FOOTER_{name}".format(name=social_name.upper()),
                config,
                {"SOCIALMEDIA_FOOTER_{name}".format(name=social_name.upper()): False}
            )

def load_config_socialmedia(root, interactive=True):
    defaults = grvlms_config.load_defaults()
    config = grvlms_config.load_current(root, defaults)
    if interactive:
        ask_questions_socialmedia(config, defaults)
    return config, defaults

@click.command(help="socialmedia variables configuration", name="config")
@click.option("-i", "--interactive", is_flag=True, help="Run interactively")
@click.option("-s", "--set", "set_",
    type=config_cli.YamlParamType(),
    multiple=True,
    metavar="KEY=VAL", 
    help="Set a configuration value")
@click.pass_obj
def config_socialmedia(context, interactive, set_):
    config, defaults = load_config_socialmedia(
        context.root, interactive=interactive
    )
    if set_:
        grvlms_config.merge(config, dict(set_), force=True)
    grvlms_config.save_config_file(context.root, config)
    grvlms_config.merge(config, defaults)
    env.save(context.root, config)

command.add_command(print_version)
command.add_command(config_socialmedia)
