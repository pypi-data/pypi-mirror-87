import click

from awscli.completer import Completer as AwsCompleter
from .ec2 import EC2
from .elb import ELB
from .resources import Resources


# Need invoke_without_commands=True because need to call --all-commands
# without any command.
@click.group(invoke_without_command=True)
@click.option(
    "--all-commands", is_flag=True, help="List all known commands.",
)
def cli(*args, **kwargs):
    if kwargs["all_commands"]:
        for cmd in AwsCompleter().complete("aws", 3):
            click.echo(cmd)


@cli.command(help="Use tags to query EC2 instances and show their attributes.")
@click.option(
    "--attributes",
    "-a",
    default=[
        "instance_id",
        "instance_type",
        "key_name",
        "image_id",
        "private_ip_address",
        "launch_time",
    ],
    show_default=True,
    multiple=True,
    help="One or multiple attributes to show.",
)
@click.option(
    "--known-attributes",
    is_flag=True,
    help="List all known attributes by this script.",
)
@click.option(
    "--order-by",
    "-o",
    default="launch_time",
    show_default=True,
    help="Order by attribute",
)
@click.option(
    "--tag-key",
    "-k",
    multiple=True,
    default=["Name"],
    show_default=True,
    help="One or multiple tag key names. When multiple tag key names are specified, they all use the same values as specified by the --tag-value option.",
)
@click.option(
    "--tag-value",
    "-v",
    multiple=True,
    help="One or multiple tag values. If no value is specified, then all the instances that have the specified tag keys are listed.",
)
def ec2(*args, **kwargs):
    EC2(*args, **kwargs).run()


@cli.command()
@click.option(
    "--limit",
    default=0,
    show_default=True,
    help="Limit the number of results that get shown. 0 means no limit",
)
@click.option(
    "--list", "-l", is_flag=True, help="List ELBs for this account",
)
@click.option(
    "--show-limits", is_flag=True, help="Show ELB limits for this account.",
)
@click.option("--tag-key", "-k")
@click.option("--tag-value", "-v")
def elb(*args, **kwargs):
    ELB(*args, **kwargs).run()


@cli.command()
@click.option(
    "--types",
    default=[],
    multiple=True,
    help=(
        'Filter resources by types. Types can be in the form of "service" or '
        '"service:resouce_type", for example, "ec2" or "ec2:instance".'
    ),
)
@click.option(
    "--with-tags",
    help='Filter resources by specified tags. Tags can be in the form of "key:value", "key:value1,value2,..." or just "key:".',
    multiple=True,
    default=[],
)
@click.option(
    "--count-by-service", is_flag=True, help="Count resources by service name.",
)
def resources(*args, **kwargs):
    Resources(*args, **kwargs).run()


if __name__ == "__main__":
    cli()
