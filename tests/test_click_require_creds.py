# -*- coding: utf-8 -*-
import click

import click_require_creds
from click_require_creds import require_creds

click_require_creds.setup("click_require_creds_test")


def test_pass_default_params(runner):
    @click.command()
    @require_creds()
    def cli(username, password):
        click.echo(f"{username}:{password}")

    result = runner.invoke(cli, input="\n".join(["user", "passwd"]))

    assert not result.exception
    assert "user\n\nuser:passwd\n" == result.stdout

    # Now it should cache and not ask for password
    result = runner.invoke(cli, input="user")

    assert not result.exception
    assert "user\nuser:passwd\n" == result.stdout

    click_require_creds.clear_cache()


def test_pass_default_params_with_username(runner):
    @click.command()
    @click.option("--username", default="user")
    @require_creds()
    def cli(username, password):
        click.echo(f"{username}:{password}")

    result = runner.invoke(cli, input="passwd")

    assert not result.exception
    assert "\nuser:passwd\n" == result.stdout

    # Now it should cache and not ask for password
    result = runner.invoke(cli)

    assert not result.exception
    assert "user:passwd\n" == result.stdout

    click_require_creds.clear_cache()


def test_pass_custom_params(runner):
    @click.command()
    @require_creds("tokenid", "secret")
    def cli(tokenid, secret):
        click.echo(f"{tokenid}:{secret}")

    result = runner.invoke(cli, input="\n".join(["tokenid", "secret"]))

    assert not result.exception
    assert "tokenid\n\ntokenid:secret\n" == result.stdout

    # Now it should cache and not ask for password
    result = runner.invoke(cli, input="tokenid")

    assert not result.exception
    assert "tokenid\ntokenid:secret\n" == result.stdout

    click_require_creds.clear_cache()
