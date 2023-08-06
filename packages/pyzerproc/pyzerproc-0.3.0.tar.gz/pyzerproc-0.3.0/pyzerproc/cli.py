"""Console script for pyzerproc."""
import sys
from binascii import hexlify
import click
import logging

import pyzerproc


@click.group()
@click.option('-v', '--verbose', count=True,
              help="Pass once to enable pyzerproc debug logging. Pass twice "
                   "to also enable pygatt debug logging.")
def main(verbose):
    """Console script for pyzerproc."""
    logging.basicConfig()
    logging.getLogger('pyzerproc').setLevel(logging.INFO)
    if verbose >= 1:
        logging.getLogger('pyzerproc').setLevel(logging.DEBUG)
    if verbose >= 2:
        logging.getLogger('pygatt').setLevel(logging.DEBUG)


@main.command()
def discover():
    """Discover nearby lights"""
    lights = pyzerproc.discover()
    for light in lights:
        click.echo(light.address)

    return 0


@main.command()
@click.argument('address')
def turn_on(address):
    """Turn on the light with the given MAC address"""
    light = pyzerproc.Light(address)

    try:
        light.connect()
        light.turn_on()
    finally:
        light.disconnect()
    return 0


@main.command()
@click.argument('address')
def turn_off(address):
    """Turn off the light with the given MAC address"""
    light = pyzerproc.Light(address)

    try:
        light.connect()
        light.turn_off()
    finally:
        light.disconnect()
    return 0


@main.command()
@click.argument('address')
@click.argument('color')
def set_color(address, color):
    """Set the light with the given MAC address to an RRGGBB hex color"""
    light = pyzerproc.Light(address)

    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    try:
        light.connect()
        light.set_color(r, g, b)
    finally:
        light.disconnect()
    return 0


@main.command()
@click.argument('address')
def is_on(address):
    """Get the current on/off status of the light"""
    light = pyzerproc.Light(address)

    try:
        light.connect()
        state = light.get_state()
        click.echo(state.is_on)
    finally:
        light.disconnect()
    return 0


@main.command()
@click.argument('address')
def get_color(address):
    """Get the current color of the light"""
    light = pyzerproc.Light(address)

    try:
        light.connect()
        state = light.get_state()
        click.echo(hexlify(bytes(state.color)))
    finally:
        light.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
