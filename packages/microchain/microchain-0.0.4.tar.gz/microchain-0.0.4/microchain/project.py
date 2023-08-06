import sh
import os
import logging

log = logging.getLogger(__name__)

rshell = sh.rshell.bake('--quiet', '--nocolor', '--timing')

def build(project_path='.', requirements='requirements.micropython.txt', build_path='/tmp/microchain-build'):
    sh.rm('-rf', build_path, _fg=True)
    sh.mkdir('-p', build_path, _fg=True)
    sh.cp('-r', project_path, os.path.join(build_path, '.'), _fg=True)
    sh.micropython(
        '-m', 'upip', 'install',
        '-p', build_path,
        '-r', os.path.join(project_path, requirements),
        _fg=True)

def upload(build_path='/tmp/microchain-build', upload_path='/pyboard', port='/dev/ttyUSB0'):
    rshell(
        '--port', port,
        'cp', '-r', os.path.join(build_path, '*'), os.path.join(upload_path, '.'),
        _fg=True)