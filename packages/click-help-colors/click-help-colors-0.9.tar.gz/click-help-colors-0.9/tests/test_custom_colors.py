import click

from click_help_colors import HelpColorsGroup, HelpColorsCommand


def test_command_custom_colors(runner):
    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green'
    )
    def cli():
        pass

    @cli.command(
        cls=HelpColorsCommand,
        help_headers_color='red',
        help_options_color='blue'
    )
    @click.option('--name', help='The person to greet.')
    def command(name):
        pass

    result = runner.invoke(cli, ['command', '--help'], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        '\x1b[31mUsage: \x1b[0mcli command [OPTIONS]',
        '',
        '\x1b[31mOptions\x1b[0m:',
        '  \x1b[34m--name TEXT\x1b[0m  The person to greet.',
        '  \x1b[34m--help\x1b[0m       Show this message and exit.'
    ]


def test_custom_option_color(runner):
    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green',
        help_options_custom_colors={'command1': 'red'}
    )
    def cli():
        pass

    @cli.command()
    def command1(name):
        pass

    @cli.command()
    def command2(name):
        pass

    result = runner.invoke(cli, ['--help'], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        '\x1b[33mUsage: \x1b[0mcli [OPTIONS] COMMAND [ARGS]...',
        '',
        '\x1b[33mOptions\x1b[0m:',
        '  \x1b[32m--help\x1b[0m  Show this message and exit.',
        '',
        '\x1b[33mCommands\x1b[0m:',
        '  \x1b[31mcommand1\x1b[0m',
        '  \x1b[32mcommand2\x1b[0m'
    ]
