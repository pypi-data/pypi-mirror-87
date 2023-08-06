import microchain.mcu
import microchain.project
import click
import rich
import os


class _config:
    port = '/dev/ttyUSB0'
    chip = 'auto'
    flash_baud = 921600
    flash_filename = '/tmp/microchain-firmware.bin'
    terminal_baud = 115200
    project_build_path='/tmp/microchain-build'
    project_upload_path='/pyboard'
    project_path='.'
    project_requirements='requirements.micropython.txt'


@click.group(help='Toolchain for micropython and microcontrollers')
@click.option('--port', default=_config.port, help='USB Port')
@click.option('--project-path', default=_config.project_path, help='Micropython project path')
@click.pass_context
def cli(ctx, port, project_path):
    _config.port = port
    _config.project_path = project_path


@click.group(help='Manage toolchain configuration')
def config():
    pass

@config.command(help='Show configuration')
def show():
    rich.print({k: v for k, v in _config.__dict__.items() if not k.startswith('_')})

@click.group(help='Manage microcontroller')
def mcu():
    pass

@mcu.command(help='Erase flash on mcu')
def erase():
    microchain.mcu.erase_flash(
        port=_config.port,
        chip=_config.chip)

@mcu.command(help='Write firmware on mcu')
def write():
    microchain.mcu.write_flash(
        filename=_config.flash_filename,
        port=_config.port,
        chip=_config.chip,
        baud=_config.flash_baud)

@mcu.command(help='Flash firmware on mcu (erase and write)')
@click.pass_context
def flash(ctx):
    ctx.invoke(erase)
    ctx.invoke(write)

@mcu.command(help='Open serial terminal to mcu')
def terminal():
    microchain.mcu.terminal(
        port=_config.port,
        baud=_config.terminal_baud)

@mcu.command(help='List files on mcu')
def ls():
    microchain.mcu.shell(
        'ls -l',
        port=_config.port,
        baud=_config.terminal_baud)


@click.group(help='Manage micropython project')
@click.option('--path', default=_config.project_path, help='Project path')
@click.pass_context
def project(ctx, path):
    _config.project_path = path

@project.command(help='Build and upload project to mcu')
@click.pass_context
def upload(ctx):
    microchain.project.build(
        project_path=_config.project_path,
        requirements=_config.project_requirements,
        build_path=_config.project_build_path)

    microchain.project.upload(
        build_path=_config.project_build_path,
        upload_path=_config.project_upload_path,
        port=_config.port)

@project.command(help='Flash and upload project to mcu')
@click.pass_context
def deploy(ctx):
    ctx.invoke(flash)
    ctx.invoke(upload)

cli.add_command(config)
cli.add_command(mcu)
cli.add_command(project)
cli()